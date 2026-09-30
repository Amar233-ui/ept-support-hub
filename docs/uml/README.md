# Diagrammes UML

Rédigés en **Mermaid** (rendus directement par GitHub) ou en **PlantUML** si Mermaid ne suffit pas. Ils seront produits au milestone **M1 — Conception** :

- [ ] `use-cases.md` : cas d'utilisation par acteur (usager, vigile, technicien N1/N2, chef de service, admin) ;
- [ ] `class-diagram.md` : modèle du domaine (User, Service, Zone, Ticket, TicketEvent, Comment, Attachment, SlaPolicy, TemporaryRequest, Notification, AuditLog, TicketEmbedding) ;
- [ ] `ticket-state-machine.md` : diagramme d'états du ticket, avec les rôles autorisés par transition ;
- [ ] `sequences.md` : connexion OAuth, création de ticket avec IA, résolution avec cause racine, détection d'un dépassement de SLA.

Les flux principaux sont déjà esquissés dans [`../architecture.md`](../architecture.md).
