# Configurer Google OAuth 2.0

La connexion est réservée aux comptes Google Workspace **@ept.sn**. En développement, on peut s'en passer grâce au login rapide du profil `dev` (disponible à partir de M2).

## 1. Créer le projet et l'écran de consentement

1. Ouvrir https://console.cloud.google.com/ avec un compte `@ept.sn`, puis créer un projet `ept-support-hub`.
2. **API et services → Écran de consentement OAuth** :
   - type d'utilisateur : **Interne**. Seuls les comptes du domaine ept.sn peuvent se connecter, et aucune validation Google n'est nécessaire. Si l'option est grisée, votre compte n'appartient pas à l'organisation Workspace : demander au CRI ;
   - nom de l'application : `EPT Support Hub` ; email d'assistance : l'adresse du CRI ;
   - champs d'application : `openid`, `email`, `profile`.

## 2. Créer l'identifiant client

**API et services → Identifiants → Créer des identifiants → ID client OAuth** :

- type : **Application Web** ;
- nom : `EPT Support Hub (dev)`, puis un second client pour la prod.

| | Dev | Prod |
|---|---|---|
| Origines JavaScript autorisées | `http://localhost:5173` | `https://support.ept.sn` |
| URI de redirection autorisés | `http://localhost:5173/api/login/oauth2/code/google` | `https://support.ept.sn/api/login/oauth2/code/google` |

La redirection passe par l'origine du front (proxy Vite en dev, Nginx en prod) : les cookies sont ainsi posés sur la même origine que la SPA.

## 3. Renseigner `.env`

```dotenv
GOOGLE_CLIENT_ID=xxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxx
APP_ALLOWED_DOMAIN=ept.sn
```

Ne jamais committer ces valeurs. En prod, les injecter via les variables d'environnement du serveur.

## 4. Sécurité : ce que vérifie le backend

Le paramètre `hd=ept.sn` envoyé à Google ne fait que **filtrer le sélecteur de comptes** : il peut être retiré par l'utilisateur. Le backend vérifie donc systématiquement, sur l'`id_token` validé :

1. `hd == "ept.sn"` ;
2. `email` se termine par `@ept.sn` ;
3. `email_verified == true`.

Un test automatisé couvre le refus d'un compte hors domaine.
