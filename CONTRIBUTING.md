# Contribuer à EPT Support Hub

Ce guide s'adresse aux deux membres du binôme et à toute personne qui reprendrait le projet.

## Démarrage

```bash
cp .env.example .env
make setup   # installe les hooks git (lefthook) et les dépendances locales
make up      # démarre toute la stack en Docker
```

Services en dev :

| Service | URL |
|---|---|
| Frontend (Vite) | http://localhost:5173 |
| Backend (API) | http://localhost:8080/api — Swagger : http://localhost:8080/api/swagger-ui.html |
| Service IA | http://localhost:8000/docs (exposé en dev uniquement) |
| Mailpit | http://localhost:8025 |
| PostgreSQL | localhost:5432 |

## Workflow Git

1. Prendre une issue sur le board (colonne *À faire*), s'assigner, la passer *En cours*.
2. Créer une branche depuis `main` :
   - `feat/<num-issue>-slug` — fonctionnalité (ex. `feat/42-ticket-state-machine`)
   - `fix/<num-issue>-slug` — correctif
   - `chore/…`, `docs/…`, `ci/…`, `refactor/…`
3. Commits au format **Conventional Commits**, en anglais :
   ```
   feat(ticket): add explicit state machine
   fix(auth): reject non ept.sn hosted domain
   docs(adr): add 0005 storage strategy
   ```
   Scopes usuels : `auth`, `user`, `org`, `ticket`, `sla`, `request`, `ai`, `notification`, `report`, `dashboard`, `audit`, `ui`, `infra`, `ci`, `deps`.
4. Ouvrir une PR vers `main` (template pré-rempli), avec `Closes #<num>`.
5. **1 review obligatoire de l'autre binôme** + CI verte → *squash merge*.

`main` est protégée : pas de push direct.

## Conventions

- **Langue** : code, noms, commits, commentaires techniques → anglais. Tout ce que voit l'utilisateur (UI, emails, PDF, docs) → français.
- **Backend** : package par fonctionnalité (`sn.ept.supporthub.<feature>`), DTO via MapStruct, erreurs en `ProblemDetail` (RFC 7807), pagination serveur (`Pageable`) sur toute liste.
- **Migrations** : Flyway, `V<n>__description.sql`. Ne **jamais** modifier une migration déjà mergée — en créer une nouvelle.
- **API** : le contrat OpenAPI est la source de vérité. Après un changement d'API : `make api-types` puis committer `docs/openapi.json` et `frontend/src/api/schema.d.ts`.
- **Frontend** : composants génériques dans `src/components/ui`, code métier dans `src/features/<domaine>`. Couleurs uniquement via les tokens (jamais de hex en dur dans un composant).
- **IA** : chaque endpoint a un test pytest ; tout score affiché à l'utilisateur est documenté dans `docs/ai.md`.
- **Décisions d'architecture** : toute décision structurante → un ADR dans `docs/adr/`.

## Tests et lint

```bash
make test        # les 3 services
make lint        # Spotless check, ESLint + Prettier, ruff
make format      # corrige automatiquement
```

Individuellement :

```bash
cd backend && ./mvnw verify          # unitaires + intégration (Testcontainers, Docker requis)
cd frontend && npm run test && npm run lint
cd ai-service && uv run pytest && uv run ruff check .
```

## Definition of Done

Une issue est terminée quand :

- [ ] les critères d'acceptation de l'issue sont cochés ;
- [ ] les tests sont écrits et passent (CI verte) ;
- [ ] le lint passe ;
- [ ] la doc est à jour (README, `docs/`, `CLAUDE.md` si une convention change) ;
- [ ] aucun secret n'est committé ;
- [ ] pour l'UI : capture d'écran (clair + sombre) dans la PR, testé en largeur mobile ;
- [ ] la PR a été relue et approuvée par l'autre binôme.
