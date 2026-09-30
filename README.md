# EPT Support Hub

**Plateforme centralisée de gestion des incidents, de suivi des tickets et de pilotage du support** de l'École Polytechnique de Thiès. Commanditaire : Centre de Ressources Informatiques (CRI).

Aujourd'hui, les pannes sont signalées par téléphone, sur WhatsApp ou de vive voix : pas de traçabilité, pas de priorisation, pas d'indicateurs. EPT Support Hub donne à chaque membre de l'EPT un point d'entrée unique pour déclarer un incident. Les tickets sont routés automatiquement vers le bon service (CRI, Service Technique…), et l'IA de corrélation retrouve les incidents déjà résolus dans la même zone du campus.

> 🚧 Projet transversal en cours : milestone **M0 — Fondations**. Voir le [board](https://github.com/users/Amar233-ui/projects) et les [milestones](https://github.com/Amar233-ui/ept-support-hub/milestones).

## Fonctionnalités prévues

- Connexion **Google @ept.sn** uniquement, validation des comptes par l'administration
- Tickets avec **machine à états**, commentaires publics et internes, pièces jointes, historique complet
- **SLA** par service et par priorité, alertes de dépassement
- **IA** : classification et routage automatiques, suggestion d'assignation, corrélation des incidents par zone
- Notifications **temps réel**, email (et WhatsApp en option)
- **Tableaux de bord** par rôle, rapports d'intervention **PDF**, journal d'audit
- Besoins temporaires (prêt de matériel, droits réseau), séparés des incidents
- Module **vigiles** avec saisie vocale (stretch)

## Démarrage en 3 commandes

Prérequis : Docker Desktop (ou Docker Engine + Compose v2) et Git.

```bash
git clone https://github.com/Amar233-ui/ept-support-hub.git && cd ept-support-hub
cp .env.example .env
docker compose up -d --build        # ou : make up
```

| Service | URL |
|---|---|
| Application | http://localhost:5173 |
| API (Swagger) | http://localhost:8080/api/swagger-ui.html |
| Service IA (docs) | http://localhost:8000/docs |
| Emails de dev (Mailpit) | http://localhost:8025 |

Le premier démarrage prend plusieurs minutes (téléchargement des images et des dépendances Maven et npm). Les suivants prennent quelques secondes.

### Commandes utiles

| `make …` | Équivalent sans make | Effet |
|---|---|---|
| `make up` / `make down` | `docker compose up -d --build` / `docker compose down` | démarrer / arrêter |
| `make logs s=backend` | `docker compose logs -f backend` | suivre les logs |
| `make test` | voir [CONTRIBUTING](CONTRIBUTING.md#tests-et-lint) | tous les tests |
| `make lint` / `make format` | | lint / formatage des 3 services |
| `make reset-db` | | ⚠️ supprime la base de dev |

**Windows** : `make` s'installe avec `winget install ezwinports.make` (à utiliser depuis Git Bash). Sinon, les commandes `docker compose` ci-dessus suffisent.

## Stack

| Couche | Technologies |
|---|---|
| Frontend | Vue 3, Vite, TypeScript, Pinia, Tailwind CSS v4, reka-ui, Apache ECharts |
| Backend | Java 21, Spring Boot 3.5, Spring Security (OAuth2), JPA, Flyway, WebSocket STOMP |
| IA | Python 3.12, FastAPI, scikit-learn, sentence-transformers, faster-whisper |
| Données | PostgreSQL 16 + pgvector |
| Infra | Docker Compose, Nginx, GitHub Actions |

## Documentation

- [Architecture](docs/architecture.md) et [décisions (ADR)](docs/adr/README.md)
- [Design system](docs/design-system.md) (catalogue vivant : http://localhost:5173/dev/ui)
- [IA : modèles et formules](docs/ai.md)
- [API et contrat OpenAPI](docs/api.md)
- [Configurer Google OAuth](docs/setup-google-oauth.md) · [WhatsApp](docs/setup-whatsapp.md)
- [Déploiement](docs/deployment.md)
- [Contribuer](CONTRIBUTING.md)

## Dépannage

- **Le backend reste `starting` longtemps au premier lancement** : Maven télécharge ses dépendances dans le volume `m2-cache`, ce qui peut prendre plusieurs minutes sur une connexion lente. Suivre la progression avec `docker compose logs -f backend`.
- **Port déjà utilisé** : changer `POSTGRES_PORT`, `BACKEND_PORT`, `FRONTEND_PORT`… dans `.env`.
- **Hot reload inactif sous Windows** : le polling est activé pour Vite (`CHOKIDAR_USEPOLLING`) et Spring DevTools. Si le problème persiste, cloner le repo dans le système de fichiers WSL2.

## Équipe

- **Mame Goumba Amar** ([@Amar233-ui](https://github.com/Amar233-ui)) : backend, infrastructure
- **Serigne Fallou Ngom** ([@falloungom04](https://github.com/falloungom04)) : frontend, design system, IA

École Polytechnique de Thiès, projet transversal 2026-2027.
