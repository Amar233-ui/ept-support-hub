# Configurer WhatsApp Cloud API (optionnel, M6)

Par défaut, `APP_WHATSAPP_ENABLED=false` : le canal `LoggingWhatsAppChannel` écrit dans les logs le message qui *aurait* été envoyé. C'est le mode de dev et de démonstration.

## Ce qu'il faut savoir avant de commencer

- L'API Cloud de Meta exige un **compte Meta Business** et une application Meta de type *Business*.
- En mode test, Meta fournit un **numéro de test** qui ne peut écrire qu'à **5 numéros destinataires** préalablement enregistrés. C'est suffisant pour la soutenance.
- En production, les messages initiés par l'application doivent utiliser des **templates approuvés** par Meta (validation de quelques heures à quelques jours), et le numéro de l'EPT doit être vérifié.

## Étapes (mode test)

1. https://developers.facebook.com/ → **Créer une application** → type *Business*.
2. Ajouter le produit **WhatsApp** → *API Setup*.
3. Noter le **Phone number ID** et générer un **token d'accès** temporaire (24 h), ou un token permanent via un *System User*.
4. Enregistrer les numéros destinataires de test.
5. Créer les templates (en français) : `ticket_assigned`, `ticket_status_changed`, `sla_breach`.
6. Renseigner `.env` :

```dotenv
APP_WHATSAPP_ENABLED=true
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_ACCESS_TOKEN=EAAG...
```

## Préférences utilisateur

Un utilisateur doit **activer lui-même** le canal WhatsApp et renseigner son numéro dans ses préférences (consentement explicite).
