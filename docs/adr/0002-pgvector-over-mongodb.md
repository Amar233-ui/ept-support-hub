# 0002 — PostgreSQL + pgvector plutôt que MongoDB

- **Statut** : acceptée
- **Date** : 2026-09-30
- **Décideurs** : @Amar233-ui, @falloungom04

## Contexte

Le cahier des charges évoque MongoDB pour stocker l'historique des incidents et alimenter l'IA de corrélation. Cette IA doit retrouver des tickets résolus **similaires** (recherche sémantique sur des embeddings) **dans la même zone ou une zone voisine** (arbre des zones), avec leur cause racine. Les données métier (tickets, utilisateurs, SLA) sont fortement relationnelles.

## Décision

Une seule base **PostgreSQL 16 avec l'extension pgvector**. Les embeddings des tickets sont stockés dans une colonne `vector(384)` (modèle multilingue MiniLM), avec un index HNSW. La recherche combine similarité cosinus et filtre sur zone en **une seule requête SQL**.

## Alternatives considérées

- **PostgreSQL + MongoDB** : deux moteurs à sauvegarder, à migrer, à superviser et à apprendre ; synchronisation des tickets vers Mongo (double écriture ou CDC) ; aucune jointure possible entre zone, ticket et vecteur.
- **Base vectorielle dédiée (Qdrant, Weaviate)** : performante, mais un service de plus, et des volumes (quelques milliers de tickets) très loin de ce qui justifie un moteur spécialisé.
- **Recherche TF-IDF en mémoire côté Python** : simple, mais sans persistance et sans jointure sur les zones.

## Conséquences

- Moins de services à maintenir à deux : un seul `docker-compose`, une seule sauvegarde, un seul outil de migration (Flyway).
- Les requêtes de corrélation restent lisibles et testables avec Testcontainers (même image `pgvector/pgvector:pg16`).
- Limite : au-delà de plusieurs millions de vecteurs, il faudrait réévaluer. Hors sujet pour l'EPT.
- Le service IA a un accès **en lecture** aux tickets et en écriture sur la seule table des embeddings ; les migrations restent la propriété du backend.
