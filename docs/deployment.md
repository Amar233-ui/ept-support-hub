# Déploiement

> Guide initial (M0). Il sera complété et éprouvé au milestone M7 : hébergement cible, TLS, sauvegardes.

## Prérequis serveur

- Linux avec Docker Engine et le plugin Compose v2 ; 4 Go de RAM minimum (8 Go recommandés avec le speech-to-text).
- Un nom de domaine (ex. `support.ept.sn`) et un certificat TLS : certbot sur l'hôte, ou un reverse proxy TLS en amont fourni par le CRI.

## Mise en route

```bash
git clone https://github.com/Amar233-ui/ept-support-hub.git && cd ept-support-hub
cp .env.example .env    # puis renseigner TOUTES les valeurs de prod (voir ci-dessous)
docker compose -f infra/docker-compose.prod.yml --env-file .env up -d --build
```

Variables à changer impérativement en prod : `SPRING_PROFILES_ACTIVE=prod`, `POSTGRES_PASSWORD`, `APP_JWT_SECRET` (`openssl rand -base64 48`), `AI_INTERNAL_TOKEN`, `GOOGLE_CLIENT_ID/SECRET` (client de prod), `APP_FRONTEND_URL=https://support.ept.sn`, `MAIL_*`.

## Topologie

- Seul **Nginx** publie un port (80, et 443 si TLS est terminé sur l'hôte).
- PostgreSQL, le backend et le service IA sont sur un réseau Docker interne, sans port exposé.
- `/api` et `/ws` sont proxifiés vers le backend ; tout le reste est servi par l'image du front.

## Sauvegardes (à mettre en place en M7)

```bash
docker compose -f infra/docker-compose.prod.yml exec -T postgres \
  pg_dump -U supporthub -Fc supporthub > backup-$(date +%F).dump
```

Plus le volume `storage` (pièces jointes, PDF).

## Mise à jour

```bash
git pull
docker compose -f infra/docker-compose.prod.yml up -d --build
```

Les migrations Flyway s'appliquent au démarrage du backend.
