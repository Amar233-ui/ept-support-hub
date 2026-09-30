# 0003 — STOMP sur WebSocket plutôt que Socket.IO

- **Statut** : acceptée
- **Date** : 2026-09-30
- **Décideurs** : @Amar233-ui, @falloungom04

## Contexte

Le cahier des charges cite Socket.IO pour les notifications temps réel. Le backend est en Spring Boot.

## Décision

Utiliser **WebSocket + STOMP** via `spring-boot-starter-websocket` (broker simple en mémoire), et `@stomp/stompjs` côté front. Destinations :

- `/user/queue/notifications` : notifications personnelles ;
- `/topic/services/{serviceId}/tickets` : mises à jour des files de traitement d'un service.

L'authentification du handshake réutilise le cookie JWT HttpOnly ; l'abonnement à un topic de service est autorisé côté serveur selon le rôle et le service.

## Alternatives considérées

- **Socket.IO** : protocole propriétaire. Côté Java, il faut `netty-socketio`, non maintenu activement, en dehors de Spring Security, sur un second port. Risque élevé pour un bénéfice nul.
- **Server-Sent Events** : suffisant pour du push serveur → client, mais pas de routage par destination ni d'intégration STOMP ; on perdrait les abonnements par service.
- **Polling** : simple, mais pas de temps réel et charge inutile.

## Conséquences

- Intégration native avec Spring Security et l'authentification existante.
- Le front gère la reconnexion automatique (option de `@stomp/stompjs`).
- Le broker en mémoire ne fonctionne qu'avec une seule instance du backend. C'est suffisant pour l'EPT. Pour passer à plusieurs instances, il faudrait un relais vers RabbitMQ (piste v2).
