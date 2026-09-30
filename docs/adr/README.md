# Architecture Decision Records

Une décision structurante = un ADR court, numéroté, jamais réécrit : si la décision change, on crée un nouvel ADR qui *remplace* l'ancien.

Modèle : [`template.md`](template.md).

| # | Décision | Statut |
|---|---|---|
| [0001](0001-monorepo.md) | Monorepo pour les trois services | Acceptée |
| [0002](0002-pgvector-over-mongodb.md) | PostgreSQL + pgvector plutôt que MongoDB | Acceptée |
| [0003](0003-stomp-over-socketio.md) | STOMP sur WebSocket plutôt que Socket.IO | Acceptée |
| [0004](0004-auth-httponly-cookie.md) | OAuth Google côté serveur + JWT en cookie HttpOnly | Acceptée |
| [0005](0005-spring-boot-3-5.md) | Rester sur Spring Boot 3.5 pour le semestre | Acceptée |
