# 0004 — OAuth Google côté serveur + JWT en cookie HttpOnly

- **Statut** : acceptée
- **Date** : 2026-09-30
- **Décideurs** : @Amar233-ui, @falloungom04

## Contexte

La connexion se fait **exclusivement** avec un compte Google `@ept.sn`. La SPA Vue doit appeler l'API de façon authentifiée, et le WebSocket doit être authentifié lui aussi. On veut limiter l'impact d'une faille XSS.

## Décision

1. Le **backend** gère le flow OAuth 2.0 / OpenID Connect (`oauth2Login` de Spring Security, paramètre `hd=ept.sn`).
2. À la réception de l'`id_token`, le backend vérifie **le claim `hd == "ept.sn"` ET que l'email se termine par `@ept.sn` et est vérifié** (`email_verified`). Le paramètre `hd` envoyé à Google n'est qu'un indice d'interface, il ne constitue pas une garantie.
3. Le backend émet :
   - un **access token JWT** (15 min) dans un cookie `HttpOnly; Secure; SameSite=Lax; Path=/api` ;
   - un **refresh token** opaque (7 jours), stocké haché en base (révocable, rotation à chaque usage), dans un cookie `HttpOnly; Secure; SameSite=Lax; Path=/api/auth/refresh`.
4. Aucun token n'est accessible en JavaScript ni stocké dans le `localStorage`.
5. Le **CSRF** reste activé : `CookieCsrfTokenRepository` pose un cookie `XSRF-TOKEN` lisible, renvoyé par le front dans l'en-tête `X-XSRF-TOKEN` pour toute requête non-GET.
6. Profil `dev` uniquement : `POST /api/dev/login-as/{seedUser}` pour se connecter avec un compte de seed. Le bean est annoté `@Profile("dev")`, et un test démarre le profil `prod` pour vérifier que l'endpoint renvoie 404.

## Alternatives considérées

- **Token dans le localStorage + en-tête `Authorization`** : exposé à toute XSS, et impossible à poser sur le handshake WebSocket du navigateur sans le passer en query string.
- **Session serveur classique (JSESSIONID)** : simple et robuste, mais complique la montée en charge et se marie moins bien avec le WebSocket et d'éventuels clients mobiles. Reste une alternative valable si le JWT pose problème.
- **Google Sign-In côté front puis envoi de l'id_token au backend** : la vérification repose sur une étape de plus, et la logique d'auth se retrouve dans le front.

## Conséquences

- La protection CSRF est obligatoire et doit être testée.
- `SameSite=Lax` suffit car front et API partagent la même origine en prod (Nginx) et en dev (proxy Vite).
- Déconnexion = suppression des cookies + révocation du refresh token en base.
- La suspension d'un compte prend effet au plus tard à l'expiration de l'access token (15 min). Si c'est jugé trop long, il faudra une vérification du statut à chaque requête (cache court).
