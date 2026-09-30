# 0001 — Monorepo pour les trois services

- **Statut** : acceptée
- **Date** : 2026-09-30
- **Décideurs** : @Amar233-ui, @falloungom04

## Contexte

Le projet comporte un backend Spring Boot, un frontend Vue et un micro-service IA Python. Deux personnes le développent pendant un semestre. La plupart des fonctionnalités sont verticales : une création de ticket touche le back, le front et parfois l'IA.

## Décision

Un seul dépôt GitHub `ept-support-hub` avec `backend/`, `frontend/` et `ai-service/`, une CI par service filtrée par chemin, un seul board et une seule série de milestones.

## Alternatives considérées

- **Trois dépôts** : versions indépendantes, mais trois boards, trois jeux de conventions, des PR croisées difficiles à relire ensemble, et un contrat OpenAPI à synchroniser à la main.
- **Monorepo avec outil de build unifié (Nx, Bazel)** : trop lourd pour deux personnes et trois langages.

## Conséquences

- Une fonctionnalité verticale peut être livrée et relue dans une seule PR si elle est petite.
- Le contrat OpenAPI (`docs/openapi.json`) et les types TypeScript générés vivent au même endroit ; la CI détecte leur divergence.
- Les workflows doivent filtrer par chemin pour rester rapides (fait au niveau des jobs, afin que les checks obligatoires s'exécutent toujours).
- `CODEOWNERS` reflète la répartition, mais toute PR peut être relue par l'autre binôme.
