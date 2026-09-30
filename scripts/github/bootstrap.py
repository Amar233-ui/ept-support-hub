"""Apply scripts/github/issues.yml to a GitHub repository with the gh CLI.

Idempotent: labels are upserted, milestones matched by title, issues matched by a hidden
`<!-- issue-id: Mx-yy -->` marker (fallback: title). Existing issues are never rewritten
(labels, milestone and body edited on GitHub are kept); a re-run only creates what is
missing, resolves pending cross-references and adds missing assignees.

Default mode is a DRY RUN that prints a summary. Use --apply to change anything.
Run through scripts/github/bootstrap.sh (handles the Python/uv environment).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PROJECT_TITLE = "EPT Support Hub"
BOARD_COLUMNS = [  # (name, color, description)
    ("Backlog", "GRAY", "Planifié, pas encore dans le sprint"),
    ("À faire (sprint)", "BLUE", "Sélectionné pour le sprint en cours"),
    ("En cours", "YELLOW", "Quelqu'un travaille dessus"),
    ("En review", "PURPLE", "PR ouverte, en attente de relecture"),
    ("Terminé", "GREEN", "Mergé et fermé"),
]
REQUIRED_CHECKS = ["backend", "frontend", "ai-service"]
MARKER = re.compile(r"<!-- issue-id: (\S+) -->")
REF = re.compile(r"\{\{(M\d-\d{2})\}\}")


# --------------------------------------------------------------------------- gh helpers
NETWORK_ERRORS = ("error connecting", "timeout", "connection", "EOF", "502", "503", "504")


def gh(*args: str, input_data: str | None = None, check: bool = True) -> str:
    # Network hiccups are retried, except for issue creation where a lost response could
    # create a duplicate (a re-run of the script will pick up anything missing instead).
    retries = 1 if args[:2] == ("issue", "create") else 5
    for attempt in range(1, retries + 1):
        result = subprocess.run(["gh", *args], input=input_data, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0 or not any(e in result.stderr for e in NETWORK_ERRORS):
            break
        if attempt < retries:
            print(f"    … erreur réseau, nouvelle tentative ({attempt}/{retries - 1})")
            time.sleep(5 * attempt)
    if check and result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])}… failed:\n{result.stderr.strip()}")
    return result.stdout


def gh_json(*args: str, input_data: str | None = None):
    out = gh(*args, input_data=input_data)
    return json.loads(out) if out.strip() else None


# --------------------------------------------------------------------------- model
def load_plan() -> dict:
    plan = yaml.safe_load((HERE / "issues.yml").read_text(encoding="utf-8"))
    ids = [i["id"] for i in plan["issues"]]
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    if dupes:
        sys.exit(f"Duplicate issue ids: {dupes}")
    titles = [i["title"] for i in plan["issues"]]
    if len(set(titles)) != len(titles):
        sys.exit("Duplicate issue titles (titles must be unique)")
    known = set(ids)
    for issue in plan["issues"]:
        for ref in issue.get("related", []) + issue.get("depends", []):
            if ref not in known:
                sys.exit(f"{issue['id']} references unknown issue {ref}")
    return plan


def issue_labels(issue: dict) -> list[str]:
    labels = [f"type:{issue['type']}", f"prio:{issue['prio']}", f"size:{issue['size']}"]
    labels += [f"area:{a}" for a in issue["area"]]
    return labels + issue.get("extra_labels", [])


def render_body(issue: dict, numbers: dict[str, int]) -> str:
    def ref(issue_id: str) -> str:
        return f"#{numbers[issue_id]}" if issue_id in numbers else f"{{{{{issue_id}}}}}"

    size_label = {"S": "S (≤ 0,5 j)", "M": "M (≈ 1 j)", "L": "L (≈ 2 j)"}[issue["size"]]
    lines = ["## Contexte", "", issue["context"].strip(), "", "## Critères d'acceptation", ""]
    lines += [f"- [{'x' if issue.get('done') else ' '}] {c}" for c in issue["criteria"]]
    if issue.get("depends") or issue.get("related"):
        lines += ["", "## Liens", ""]
        if issue.get("depends"):
            lines.append("- Bloquée par : " + ", ".join(ref(d) for d in issue["depends"]))
        if issue.get("related"):
            lines.append("- Liée à : " + ", ".join(ref(r) for r in issue["related"]))
    lines += ["", f"_Estimation : {size_label}._", "", f"<!-- issue-id: {issue['id']} -->"]
    return "\n".join(lines)


# --------------------------------------------------------------------------- summary
def print_summary(plan: dict) -> None:
    people = plan["people"]
    milestones = {m["key"]: m for m in plan["milestones"]}
    by_ms: dict[str, Counter] = defaultdict(Counter)
    for issue in plan["issues"]:
        by_ms[issue["milestone"]][people[issue["assignee"]]] += 1
        by_ms[issue["milestone"]]["done"] += int(bool(issue.get("done")))

    names = list(people.values())
    header = f"{'Milestone':<34} {'Échéance':<11} {'Total':>5} " + " ".join(f"{n:>13}" for n in names)
    print(header + f" {'déjà livrées':>13}")
    print("-" * len(header + " " * 14))
    totals: Counter = Counter()
    for key, ms in milestones.items():
        c = by_ms[key]
        total = sum(c[n] for n in names)
        totals.update({**{n: c[n] for n in names}, "total": total, "done": c["done"]})
        cols = " ".join(f"{c[n]:>13}" for n in names)
        print(f"{ms['title']:<34} {ms['due']:<11} {total:>5} {cols} {c['done']:>13}")
    cols = " ".join(f"{totals[n]:>13}" for n in names)
    print("-" * len(header + " " * 14))
    print(f"{'TOTAL':<34} {'':<11} {totals['total']:>5} {cols} {totals['done']:>13}")

    size_days = {"S": 0.5, "M": 1, "L": 2}
    effort: Counter = Counter()
    for issue in plan["issues"]:
        if not issue.get("done"):
            effort[people[issue["assignee"]]] += size_days[issue["size"]]
    print("\nCharge estimée restante (jours) : " + ", ".join(f"{n} {d:g}" for n, d in effort.items()))
    print(f"Labels : {len(plan['labels'])} · Milestones : {len(plan['milestones'])}")


# --------------------------------------------------------------------------- apply steps
def ensure_collaborators(repo: str, plan: dict, owner: str) -> None:
    for login in plan["people"].values():
        if login.lower() == owner.lower():
            continue
        status = subprocess.run(["gh", "api", f"repos/{repo}/collaborators/{login}"], capture_output=True, text=True)
        if status.returncode == 0:
            print(f"  = collaborateur {login}")
            continue
        gh("api", "-X", "PUT", f"repos/{repo}/collaborators/{login}", "-f", "permission=push")
        print(f"  + invitation envoyée à {login} (à accepter pour pouvoir être assigné)")


def ensure_labels(repo: str, plan: dict) -> None:
    existing = {
        lab["name"]: lab
        for lab in gh_json("label", "list", "--repo", repo, "--limit", "300", "--json", "name,color,description")
    }
    for label in plan["labels"]:
        current = existing.get(label["name"])
        if (
            current
            and current["color"].lower() == label["color"].lower()
            and (current["description"] or "") == label["description"]
        ):
            continue
        gh(
            "label",
            "create",
            label["name"],
            "--repo",
            repo,
            "--color",
            label["color"],
            "--description",
            label["description"],
            "--force",
        )
        print(f"  {'~' if current else '+'} label {label['name']}")


def ensure_milestones(repo: str, plan: dict) -> dict[str, str]:
    existing = {m["title"]: m for m in gh_json("api", f"repos/{repo}/milestones?state=all&per_page=100")}
    titles: dict[str, str] = {}
    for ms in plan["milestones"]:
        due_on = f"{ms['due']}T23:59:59Z"
        current = existing.get(ms["title"])
        titles[ms["key"]] = ms["title"]
        if current is None:
            gh(
                "api",
                f"repos/{repo}/milestones",
                "-f",
                f"title={ms['title']}",
                "-f",
                f"due_on={due_on}",
                "-f",
                f"description={ms['description']}",
            )
            print(f"  + milestone {ms['title']}")
        elif (current.get("due_on") or "")[:10] != ms["due"] or current.get("description") != ms["description"]:
            gh(
                "api",
                "-X",
                "PATCH",
                f"repos/{repo}/milestones/{current['number']}",
                "-f",
                f"due_on={due_on}",
                "-f",
                f"description={ms['description']}",
            )
            print(f"  ~ milestone {ms['title']}")
    return titles


def ensure_issues(repo: str, plan: dict, ms_titles: dict[str, str]) -> dict[str, dict]:
    people = plan["people"]
    existing = gh_json(
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "all",
        "--limit",
        "1000",
        "--json",
        "number,title,body,state,assignees,url",
    )
    by_marker = {}
    by_title = {}
    for gi in existing:
        m = MARKER.search(gi["body"] or "")
        if m:
            by_marker[m.group(1)] = gi
        by_title[gi["title"]] = gi

    found: dict[str, dict] = {}
    for issue in plan["issues"]:
        gi = by_marker.get(issue["id"]) or by_title.get(issue["title"])
        if gi:
            found[issue["id"]] = gi

    numbers = {iid: gi["number"] for iid, gi in found.items()}

    # Pass 1: create missing issues
    for issue in plan["issues"]:
        if issue["id"] in found:
            continue
        args = [
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            issue["title"],
            "--body-file",
            "-",
            "--milestone",
            ms_titles[issue["milestone"]],
        ]
        for label in issue_labels(issue):
            args += ["--label", label]
        body = render_body(issue, numbers)
        assignee = people[issue["assignee"]]
        try:
            url = gh(*args, "--assignee", assignee, input_data=body).strip()
        except RuntimeError:
            url = gh(*args, input_data=body).strip()
            print(f"    ! {issue['id']} créée sans assigné ({assignee} n'a pas encore accepté l'invitation)")
        number = int(url.rstrip("/").rsplit("/", 1)[-1])
        numbers[issue["id"]] = number
        found[issue["id"]] = {"number": number, "url": url, "body": body, "assignees": [], "new": True}
        print(f"  + #{number} [{issue['id']}] {issue['title']}")
        if issue.get("done"):
            gh(
                "issue",
                "close",
                str(number),
                "--repo",
                repo,
                "--reason",
                "completed",
                "--comment",
                "Livré lors de l'initialisation du projet.",
            )

    # Pass 2: resolve cross-references ({{Mx-yy}} -> #n) that pointed to issues created later.
    # Only placeholders are replaced, so edits made on GitHub (ticked boxes...) are preserved.
    def resolve(match: re.Match) -> str:
        issue_id = match.group(1)
        return f"#{numbers[issue_id]}" if issue_id in numbers else match.group(0)

    for issue in plan["issues"]:
        gi = found[issue["id"]]
        current = gi.get("body") or ""
        resolved = REF.sub(resolve, current)
        if resolved != current:
            gh("issue", "edit", str(gi["number"]), "--repo", repo, "--body-file", "-", input_data=resolved)
        assignee = people[issue["assignee"]]
        if not gi.get("new") and not any(a["login"] == assignee for a in gi.get("assignees", [])):
            result = subprocess.run(
                ["gh", "issue", "edit", str(gi["number"]), "--repo", repo, "--add-assignee", assignee],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print(f"  ~ #{gi['number']} assignée à {assignee}")
    return found


def ensure_project(owner: str, repo: str, plan: dict, found: dict[str, dict]) -> None:
    projects = gh_json("project", "list", "--owner", owner, "--format", "json", "--limit", "100")["projects"]
    project = next((p for p in projects if p["title"] == PROJECT_TITLE), None)
    if project is None:
        project = gh_json("project", "create", "--owner", owner, "--title", PROJECT_TITLE, "--format", "json")
        print(f"  + projet « {PROJECT_TITLE} » #{project['number']}")
        gh("project", "link", str(project["number"]), "--owner", owner, "--repo", repo, check=False)
    number, project_id = str(project["number"]), project["id"]

    fields = gh_json("project", "field-list", number, "--owner", owner, "--format", "json")["fields"]
    status = next(f for f in fields if f["name"] == "Status")
    if [o["name"] for o in status.get("options", [])] != [c[0] for c in BOARD_COLUMNS]:
        query = """
        mutation($fieldId: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]) {
          updateProjectV2Field(input: {fieldId: $fieldId, singleSelectOptions: $options}) {
            projectV2Field { ... on ProjectV2SingleSelectField { id options { id name } } }
          }
        }"""
        options = [{"name": n, "color": c, "description": d} for n, c, d in BOARD_COLUMNS]
        payload = json.dumps({"query": query, "variables": {"fieldId": status["id"], "options": options}})
        result = gh_json("api", "graphql", "--input", "-", input_data=payload)
        status["options"] = result["data"]["updateProjectV2Field"]["projectV2Field"]["options"]
        print("  ~ colonnes du board : " + " | ".join(c[0] for c in BOARD_COLUMNS))
    option_id = {o["name"]: o["id"] for o in status["options"]}

    items = gh_json("project", "item-list", number, "--owner", owner, "--format", "json", "--limit", "1000")
    in_project = {it["content"].get("number") for it in items["items"] if it.get("content")}
    added = 0
    for issue in plan["issues"]:
        gi = found[issue["id"]]
        if gi["number"] in in_project:
            continue
        url = gi.get("url") or f"https://github.com/{repo}/issues/{gi['number']}"
        item = gh_json("project", "item-add", number, "--owner", owner, "--url", url, "--format", "json")
        column = "Terminé" if issue.get("done") else ("À faire (sprint)" if issue["milestone"] == "M0" else "Backlog")
        gh(
            "project",
            "item-edit",
            "--id",
            item["id"],
            "--project-id",
            project_id,
            "--field-id",
            status["id"],
            "--single-select-option-id",
            option_id[column],
        )
        added += 1
    if added:
        print(f"  + {added} issue(s) ajoutée(s) au projet")
    print(f"  → https://github.com/users/{owner}/projects/{number}")


def ensure_repo_settings(repo: str) -> None:
    gh(
        "api",
        "-X",
        "PATCH",
        f"repos/{repo}",
        "-F",
        "allow_squash_merge=true",
        "-F",
        "allow_merge_commit=false",
        "-F",
        "allow_rebase_merge=false",
        "-F",
        "delete_branch_on_merge=true",
        "-F",
        "has_projects=true",
    )
    protection = {
        "required_status_checks": {"strict": False, "contexts": REQUIRED_CHECKS},
        "enforce_admins": False,
        "required_pull_request_reviews": {"required_approving_review_count": 1, "dismiss_stale_reviews": True},
        "restrictions": None,
        "required_conversation_resolution": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }
    gh("api", "-X", "PUT", f"repos/{repo}/branches/main/protection", "--input", "-", input_data=json.dumps(protection))
    print(f"  = main protégée (1 review, checks {', '.join(REQUIRED_CHECKS)}), squash merge uniquement")


# --------------------------------------------------------------------------- main
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default="Amar233-ui/ept-support-hub")
    parser.add_argument("--apply", action="store_true", help="really create/update on GitHub")
    parser.add_argument("--list", action="store_true", help="also list every issue title")
    parser.add_argument("--skip-project", action="store_true")
    parser.add_argument("--skip-protection", action="store_true")
    args = parser.parse_args()

    plan = load_plan()
    print_summary(plan)
    if args.list:
        for issue in plan["issues"]:
            flag = "✓" if issue.get("done") else " "
            print(f"  {flag} {issue['id']} [{plan['people'][issue['assignee']]:<13}] {issue['title']}")

    if not args.apply:
        print("\nDRY RUN : rien n'a été modifié. Relancer avec --apply pour appliquer sur", args.repo)
        return

    owner = args.repo.split("/")[0]
    print(f"\nApplication sur {args.repo}")
    print("• Collaborateurs")
    ensure_collaborators(args.repo, plan, owner)
    print("• Labels")
    ensure_labels(args.repo, plan)
    print("• Milestones")
    ms_titles = ensure_milestones(args.repo, plan)
    print("• Issues")
    found = ensure_issues(args.repo, plan, ms_titles)
    if not args.skip_project:
        print("• Projet")
        ensure_project(owner, args.repo, plan, found)
        print("  ⚠ La vue « Board » se crée à la main : projet → New view → Board (colonnes = Status).")
    if not args.skip_protection:
        print("• Réglages du repo")
        ensure_repo_settings(args.repo)
    print("\nTerminé.")


if __name__ == "__main__":
    main()
