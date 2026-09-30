# 0005 — Rester sur Spring Boot 3.5 pour le semestre

- **Statut** : acceptée
- **Date** : 2026-09-30
- **Décideurs** : @Amar233-ui, @falloungom04

## Contexte

Le cahier des charges impose Spring Boot 3.x. En septembre 2026, la branche 4.x est la ligne principale (start.spring.io ne propose plus la 3.5), et le support open source de la 3.5 touche à sa fin.

## Décision

Rester sur **Spring Boot 3.5.x** (dernier patch : 3.5.16), avec les versions compatibles : springdoc 2.8.x, Resilience4j `-spring-boot3`.

## Alternatives considérées

- **Spring Boot 4.x** : support long, mais non conforme au cahier des charges, écosystème encore en migration (Jackson 3, modularisation des starters), moins de ressources pédagogiques.

## Conséquences

- Conformité au cahier des charges et stabilité pour le semestre.
- Dependabot doit être surveillé : on accepte les patchs 3.5.x, on refuse les montées de version majeure.
- **Piste v2** : migrer vers Spring Boot 4 après la soutenance (guide de migration officiel).
