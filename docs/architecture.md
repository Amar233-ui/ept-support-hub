# Architecture

EPT Support Hub est une application web composée de trois services applicatifs et d'une base unique, livrée sous forme de monorepo ([ADR 0001](adr/0001-monorepo.md)).

## Contexte (C4 — niveau 1)

```mermaid
flowchart LR
    user["Usager EPT<br/>(étudiant, PER, PATS)"]
    guard["Vigile"]
    tech["Technicien N1/N2"]
    head["Chef de service"]
    admin["Administrateur"]

    hub["EPT Support Hub"]

    google["Google Workspace<br/>(OAuth @ept.sn)"]
    mail["Serveur SMTP"]
    wa["WhatsApp Cloud API<br/>(optionnel)"]

    user & guard & tech & head & admin -->|navigateur| hub
    hub -->|authentification| google
    hub -->|notifications| mail
    hub -.->|notifications, feature flag| wa
```

## Conteneurs (C4 — niveau 2)

```mermaid
flowchart TB
    browser["Navigateur<br/>Vue 3 SPA"]

    subgraph prod["Hôte Docker (prod)"]
        nginx["Nginx<br/>reverse proxy + fichiers statiques"]
        backend["Backend<br/>Spring Boot 3.5 / Java 21"]
        ai["Service IA<br/>FastAPI / Python 3.12<br/>(réseau interne uniquement)"]
        db[("PostgreSQL 16<br/>+ pgvector")]
        files[("Volume fichiers<br/>pièces jointes, PDF")]
    end

    browser -->|HTTPS| nginx
    nginx -->|/api| backend
    nginx -->|/ws STOMP| backend
    backend -->|JDBC| db
    backend --> files
    backend -->|HTTP interne<br/>timeout 2 s, circuit breaker| ai
    ai -->|lecture tickets résolus,<br/>écriture embeddings| db
```

Principes :

- **Le backend est le seul point d'entrée métier.** Le front ne parle jamais au service IA ; le service IA n'est pas exposé par Nginx.
- **Dégradation gracieuse** : si l'IA ne répond pas, le ticket est créé quand même et part dans la file manuelle du chef de service.
- **Une seule base** : relationnel, vecteurs et historique des causes racines ([ADR 0002](adr/0002-pgvector-over-mongodb.md)).
- **Auth** : OAuth Google géré par le backend, session portée par un JWT court dans un cookie HttpOnly ([ADR 0004](adr/0004-auth-httponly-cookie.md)).
- **Temps réel** : STOMP sur WebSocket ([ADR 0003](adr/0003-stomp-over-socketio.md)).

## Backend — découpage par fonctionnalité

```
sn.ept.supporthub
├── auth           OAuth2 Google, JWT cookie, refresh, login dev
├── user           comptes, rôles, statut PENDING/ACTIVE/SUSPENDED, compétences
├── organization   services (configurables), zones (arbre)
├── ticket         incidents, machine à états, commentaires, pièces jointes, historique
├── sla            politiques service × priorité, job de détection
├── request        besoins temporaires (entité séparée des incidents)
├── ai             client HTTP vers le service IA (Resilience4j)
├── notification   NotificationChannel : in-app (STOMP), email, WhatsApp
├── report         PDF (Thymeleaf + OpenHTMLtoPDF)
├── dashboard      requêtes d'agrégation KPI
├── audit          journal des actions sensibles
└── common         config, erreurs ProblemDetail, pagination, storage
```

Chaque package contient ses contrôleurs, services, entités, repositories et DTO. Un package n'accède aux entités d'un autre qu'à travers son service public.

## Flux principaux

### Connexion

```mermaid
sequenceDiagram
    actor U as Usager
    participant F as Front
    participant B as Backend
    participant G as Google

    U->>F: « Se connecter avec Google »
    F->>B: GET /api/oauth2/authorization/google
    B->>G: redirection (hd=ept.sn)
    G-->>B: code d'autorisation
    B->>G: échange code → id_token
    B->>B: vérifie hd == ept.sn ET email @ept.sn
    alt premier login
        B->>B: crée le compte PENDING
    end
    B-->>F: Set-Cookie access (HttpOnly) + refresh, redirection
    F->>B: GET /api/me
    B-->>F: profil (statut, rôle)
    F-->>U: tableau de bord ou « compte en attente »
```

### Création d'un ticket avec IA

```mermaid
sequenceDiagram
    actor U as Usager
    participant B as Backend
    participant A as Service IA
    participant T as Technicien

    U->>B: POST /api/tickets
    B->>B: enregistre CREATED
    B->>A: POST /classify + /suggest-assignee (timeout 2 s)
    alt confiance ≥ seuil
        A-->>B: catégorie, service, technicien, explications
        B->>B: ASSIGNED
        B-)T: notification (in-app, email)
    else IA indisponible ou confiance faible
        B->>B: file manuelle du chef de service
    end
    B-->>U: 201 + référence INC-2026-000123
```

## Environnements

| | Dev (`docker-compose.yml`) | Prod (`infra/docker-compose.prod.yml`) |
|---|---|---|
| Front | Vite dev server, HMR | fichiers statiques derrière Nginx |
| Backend | `spring-boot:run` + DevTools, profil `dev` | JAR en couches, profil `prod`, non-root |
| IA | `uvicorn --reload`, port exposé | 2 workers, réseau interne seulement |
| DB | port 5432 exposé | aucun port exposé |
| Mail | Mailpit | SMTP réel |
