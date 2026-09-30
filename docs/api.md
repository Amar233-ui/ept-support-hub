# API

Le **contrat OpenAPI** est la source de vérité de l'API. Il est généré par springdoc à partir du code du backend.

| | URL (dev) |
|---|---|
| Swagger UI | http://localhost:8080/api/swagger-ui.html |
| JSON | http://localhost:8080/api/v3/api-docs |
| Version committée | [`docs/openapi.json`](openapi.json) (à partir de M1) |

Swagger est désactivé en profil `prod`.

## Régénérer les types du frontend

Après toute modification d'API côté backend :

```bash
make up            # le backend doit tourner
make api-types     # exporte docs/openapi.json puis génère frontend/src/api/schema.d.ts
git add docs/openapi.json frontend/src/api/schema.d.ts
```

La CI frontend régénère les types à partir de `docs/openapi.json` et échoue s'ils diffèrent de ceux committés.

## Conventions

- Préfixe `/api`, ressources au pluriel, en anglais : `/api/tickets/{id}/comments`.
- Pagination : `?page=0&size=20&sort=createdAt,desc`. La réponse contient `content` et les métadonnées de page.
- Erreurs : **RFC 7807** (`application/problem+json`), avec `type`, `title`, `status`, `detail`, et `errors[]` pour la validation.
- Dates en ISO-8601 UTC ; le front affiche en heure locale (Africa/Dakar).
- Requêtes non-GET : en-tête `X-XSRF-TOKEN` obligatoire (voir [ADR 0004](adr/0004-auth-httponly-cookie.md)).
