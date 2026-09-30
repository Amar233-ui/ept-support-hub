# CLAUDE.md — contexte pour les sessions Claude Code

EPT Support Hub : plateforme de gestion des incidents et tickets de l'École Polytechnique de Thiès (commanditaire : CRI). Projet noté, développé par **deux étudiants** pendant un semestre. Soutenance le **2027-01-01**. Il faut du code propre, démontrable et maintenable à deux.

## Règles de travail

- **Langue** : code, identifiants, commits, commentaires techniques en **anglais** ; tout ce qui est visible par l'utilisateur (UI, emails, PDF, docs/) en **français**.
- On travaille **issue par issue** (source : `scripts/github/issues.yml`, board GitHub). Ne pas implémenter hors du périmètre de l'issue en cours.
- Branches `feat/<num>-slug`, `fix/…`, `chore/…`, `docs/…`. **Conventional Commits** avec scope (`feat(ticket): …`). PR avec `Closes #n`, 1 review de l'autre binôme, CI verte, squash merge.
- **Demander avant toute action externe** : push, création ou modification sur GitHub, envoi de message.
- Toute décision structurante → ADR dans `docs/adr/` (ne jamais réécrire un ADR accepté : en créer un qui le remplace).
- Si une exigence paraît irréaliste pour deux personnes, le dire et proposer une v1 réduite + une piste v2.

## Architecture (détails : docs/architecture.md)

```
frontend/  (Vue 3 SPA)  --/api, /ws-->  backend/ (Spring Boot)  --HTTP interne-->  ai-service/ (FastAPI)
                                              |                                          |
                                              +------------> PostgreSQL 16 + pgvector <--+
```

- Le **backend** est le seul point d'entrée métier. Le front n'appelle jamais l'IA. L'IA n'est pas exposée publiquement (en-tête `X-Internal-Token`).
- Le backend **doit fonctionner si l'IA est down** : timeout court, Resilience4j, repli sur la file manuelle du chef de service.
- **Une seule base** (ADR 0002). Les migrations Flyway appartiennent au backend ; l'IA lit les tickets et écrit seulement `ticket_embeddings`.
- **Auth** (ADR 0004) : OAuth Google géré par le backend, vérification `hd == ept.sn` ET email `@ept.sn` côté serveur ; JWT court en cookie HttpOnly + refresh token en base ; CSRF actif (`XSRF-TOKEN` → `X-XSRF-TOKEN`). **Jamais de token dans le localStorage.** Login rapide uniquement en profil `dev`, avec un test qui prouve son absence en `prod`.
- **Temps réel** : STOMP sur WebSocket (ADR 0003).

### Backend — `backend/` (Java 21, Spring Boot **3.5**, voir ADR 0005)

- Package **par fonctionnalité** : `sn.ept.supporthub.{auth,user,organization,ticket,sla,request,ai,notification,report,dashboard,audit,common}`. Un package n'accède aux entités d'un autre que via son service.
- Context path `/api`. Erreurs en **ProblemDetail** (RFC 7807) via `common/web/GlobalExceptionHandler`. Pagination serveur (`Pageable`) sur toute liste.
- DTO + **MapStruct** (modèle de composant `spring`). Pas d'entité JPA exposée par l'API.
- `ddl-auto=validate` : le schéma vient **uniquement** de Flyway (`src/main/resources/db/migration/V<n>__*.sql`). **Ne jamais modifier une migration mergée.**
- Machine à états des tickets : classe explicite, testée unitairement de façon exhaustive. `RESOLVED` exige une cause racine.
- Tests : unitaires `*Test` (surefire), intégration `*IT` (failsafe + Testcontainers `pgvector/pgvector:pg16`, via `TestcontainersConfiguration`). Horloge injectée (`Clock`) pour tout ce qui dépend du temps (SLA, clôture auto).
- Format : Spotless + palantir-java-format.

### Frontend — `frontend/` (Vue 3, Vite, TS, Pinia, Tailwind v4, reka-ui)

- `src/app/` (router, navigation), `src/layouts/`, `src/components/ui/` (design system générique, préfixe `Ui`), `src/components/layout/`, `src/features/<domaine>/` (écrans métier), `src/stores/`, `src/composables/`, `src/api/` (`http.ts` + `schema.d.ts` généré).
- Alias `@/` → `src/`. `<script setup lang="ts">` partout. `erasableSyntaxOnly` : pas d'enums TS ni de *parameter properties*.
- **Couleurs uniquement via les tokens** (`bg-surface`, `text-fg-muted`, `bg-accent`…), définis dans `src/styles/tokens.css` et mappés dans `main.css` (`@theme inline`). Il n'y a pas de `tailwind.config.js` (Tailwind v4). Mode sombre : classe `dark` sur `<html>` (`useTheme`).
- Tout nouveau composant `ui/` est ajouté au catalogue **`/dev/ui`** (build de dev uniquement).
- Accent unique : **vert EPT** `#1F6B4F` (sombre `#4FB98C`). Règles : docs/design-system.md.
- Mobile-first pour les écrans usager et vigile. Accessibilité AA, focus visible, clavier.
- Types API générés : `make api-types` (backend lancé) → `docs/openapi.json` + `src/api/schema.d.ts`, tous deux committés.
- Tests : Vitest + Vue Test Utils (`*.spec.ts` à côté du fichier) ; Playwright (e2e) arrive en M7.

### IA — `ai-service/` (Python 3.12, FastAPI, uv)

- `app/main.py`, `app/routers/`, `app/config.py` (variables `AI_*`). Dépendances ML ajoutées en M4 (torch CPU uniquement).
- L'« indice de récurrence » n'est **pas une probabilité** : ne jamais le nommer `probability`. Formule dans docs/ai.md, à tenir à jour.
- Tests pytest ; lint ruff (line-length 110).

## Commandes

```bash
cp .env.example .env && make up      # stack de dev complète (ou docker compose up -d --build)
make logs s=backend                   # logs d'un service
make test | make lint | make format   # les 3 services

cd backend && ./mvnw verify           # tests back (Docker requis pour Testcontainers)
cd backend && ./mvnw spotless:apply
cd frontend && npm run test && npm run lint && npm run typecheck
cd ai-service && uv run pytest && uv run ruff check .

scripts/github/bootstrap.sh [--list]  # dry run de la planification GitHub
scripts/github/bootstrap.sh --apply   # applique (demander d'abord !)
```

URLs de dev : front :5173 · API :8080/api (Swagger `/api/swagger-ui.html`) · IA :8000/docs · Mailpit :8025.

## Environnement connu

- Postes Windows 11 : utiliser Git Bash ; `make` n'est pas installé par défaut (`winget install ezwinports.make`) ; uv via `pip install uv` (`python -m uv`).
- Connexion réseau parfois très lente : les premiers `mvn`, `npm install` et pulls Docker peuvent prendre de 10 à 20 minutes.
- Rôles : `USER` (sous-types étudiant/PER/PATS), `GUARD`, `TECH_N1`, `TECH_N2`, `SERVICE_HEAD`, `ADMIN`.
- Répartition : @Amar233-ui = backend cœur + infra ; @falloungom04 = frontend, design system, IA, vigiles.
