# Design system

Objectif : une interface **sobre, dense quand il le faut, calme** : fonds chauds, beaucoup d'espace, un seul accent. Inspirations : Linear, Jira Service Management, Zendesk, Height, l'interface de Claude. On reprend leurs principes, pas leurs marques.

Catalogue vivant : **`/dev/ui`** (build de dev uniquement). Tout nouveau composant de `src/components/ui/` doit y figurer, avec ses variantes.

## 1. Tokens

Définis dans [`frontend/src/styles/tokens.css`](../frontend/src/styles/tokens.css) (variables CSS sur `:root` et `.dark`), puis exposés à Tailwind v4 dans le bloc `@theme inline` de [`main.css`](../frontend/src/styles/main.css). Tailwind v4 n'utilise plus de `tailwind.config.js` : c'est l'équivalent.

**Règle d'or : aucune couleur en dur dans un composant.** On utilise uniquement les utilitaires ci-dessous.

### Couleurs

| Token | Utilitaire | Clair | Sombre | Usage |
|---|---|---|---|---|
| `--bg` | `bg-canvas` | `#FAF9F7` | `#161513` | fond de page, sidebar |
| `--surface` | `bg-surface` | `#FFFFFF` | `#1D1C1A` | cartes, tables, modales |
| `--surface-muted` | `bg-surface-muted` | `#F4F2EE` | `#252320` | zones secondaires, skeletons |
| `--surface-hover` | `bg-surface-hover` | `#EFECE7` | `#2B2926` | survol, élément actif |
| `--border` | `border-border` | `#E7E4DE` | `#33302C` | séparateurs fins |
| `--border-strong` | `border-border-strong` | `#D6D2CA` | `#45413B` | champs au survol |
| `--fg` | `text-fg` | `#1C1B19` | `#EDEBE7` | texte principal |
| `--fg-muted` | `text-fg-muted` | `#5F5B54` | `#A8A39A` | texte secondaire (AA) |
| `--fg-subtle` | `text-fg-subtle` | `#8A857C` | `#7A756D` | placeholders, décoratif (**pas AA** : jamais pour une info essentielle) |
| `--accent` | `bg-accent` / `text-accent` | `#1F6B4F` | `#4FB98C` | **vert EPT** : action principale, lien actif, focus |
| `--accent-soft` | `bg-accent-soft` | `#E4EFE9` | `#173229` | fond d'élément sélectionné |

Couleurs sémantiques, **discrètes**, réservées aux statuts, priorités et alertes SLA : `success`, `warning`, `danger`, `info`, chacune avec sa variante `-soft` pour les fonds de badge.

### Règles d'usage de l'accent

- **Un seul bouton `primary` par écran** (l'action principale). Le reste est `secondary` ou `ghost`.
- L'accent ne sert jamais à décorer : il signale une action ou un état actif.
- Pas de dégradés, pas d'ombres portées sur les éléments au repos. Les ombres (`shadow-overlay`) sont réservées aux éléments flottants (modales, menus, palette).

### Typographie

Police : **Inter Variable**, auto-hébergée via `@fontsource-variable/inter` (pas de CDN). Échelle courte :

| Utilitaire | Taille | Usage |
|---|---|---|
| `text-2xl` | 30px | valeur de KPI |
| `text-xl` | 24px | titre de page (un par page, `font-semibold tracking-tight`) |
| `text-lg` | 20px | titre de section |
| `text-md` | 16px | texte mis en avant ; **taille minimale des champs sur mobile** (évite le zoom iOS) |
| `text-base` | 14px | texte courant de l'UI |
| `text-sm` | 13px | tables denses, métadonnées |
| `text-xs` | 12px | badges, légendes |

Nombres dans les tables et KPI : classe **`tabular`** (chiffres à chasse fixe, les colonnes restent alignées).

### Espacements et rayons

- Grille de 4px (échelle Tailwind). Padding de carte : `p-4`. Espace entre sections : `space-y-8`.
- Rayons : `rounded-sm` (6px) badges et kbd, `rounded-md` (8px) boutons et champs, `rounded-lg` (12px) cartes et modales.
- Hauteurs de contrôle : 28px (`sm`), **32px (`md`, par défaut desktop)**, 44px (`lg` : cible tactile, écrans mobiles et vigile).

## 2. Layout

- **Sidebar** gauche : 240px, repliable à 56px (état mémorisé). Sur mobile, elle devient un drawer.
- **Topbar** 56px : bascule de sidebar, recherche / **palette `Ctrl/⌘ K`**, thème, profil.
- **Contenu** centré, `max-w-6xl`, padding 16px sur mobile et 32px sur desktop.
- **Vue ticket** (M3), à la manière de Linear : 2 colonnes. À gauche, fil d'activité (description, commentaires, historique) ; à droite, 280px de métadonnées éditables (statut, priorité, assigné, zone, SLA). Sur mobile, les métadonnées passent au-dessus.
- **Mobile-first** pour les écrans usager et vigile : déclaration d'incident en moins de 30 s, un seul formulaire, gros bouton micro (≥ 64px).

## 3. Composants

| Composant | Fichier | Statut |
|---|---|---|
| Bouton (`primary`, `secondary`, `ghost`, `danger` ; `sm`, `md`, `lg`, `icon` ; `loading`) | `UiButton.vue` | ✅ M0 |
| Badge (6 tons, option `dot`) | `UiBadge.vue` | ✅ M0 |
| Carte (titre, description, actions) | `UiCard.vue` | ✅ M0 |
| État vide (icône, titre, texte, actions) | `UiEmptyState.vue` | ✅ M0 |
| Skeleton | `UiSkeleton.vue` | ✅ M0 |
| Touche clavier | `UiKbd.vue` | ✅ M0 |
| Palette de commandes | `layout/CommandPalette.vue` | ✅ M0 |
| Champ texte, textarea, select, combobox | `UiInput`, `UiSelect`… | M1 |
| Modale, drawer, menu déroulant, tooltip | reka-ui stylés | M1 |
| Toasts | `UiToaster` | M1 |
| Table dense (tri, filtres, pagination serveur) | `UiDataTable` | M1 |
| Badges métier statut / priorité / SLA | `features/ticket/…` | M3 |
| Timeline d'historique | `features/ticket/…` | M3 |
| Carte KPI, graphiques ECharts | `features/dashboard/…` | M5 |

Les composants interactifs complexes (dialog, select, combobox, tooltip, dropdown) s'appuient sur **reka-ui**, qui fournit l'accessibilité et le clavier ; nous ne faisons que les styler.

### Mapping des statuts et priorités (M3)

| Statut | Ton | | Priorité | Ton |
|---|---|---|---|---|
| Créé | neutral | | Basse | neutral |
| Assigné | info | | Moyenne | info |
| En cours | accent | | Haute | warning |
| Escaladé | warning | | Critique | danger |
| Résolu | success | | | |
| Rouvert | danger | | | |
| Clôturé | neutral | | | |

La couleur n'est jamais le seul porteur d'information : le libellé est toujours affiché.

## 4. Accessibilité (checklist PR)

- [ ] Contraste AA (4,5:1) pour tout texte porteur d'information : `fg` et `fg-muted` passent, `fg-subtle` non.
- [ ] Focus visible (anneau `--focus-ring`) sur tout élément interactif ; jamais de `outline: none` sans remplacement.
- [ ] Tout est utilisable au clavier (Tab, Entrée, Échap, flèches dans les listes).
- [ ] Boutons icônes avec `aria-label` en français.
- [ ] Animations désactivées avec `prefers-reduced-motion` (`motion-reduce:`).
- [ ] Testé en mode clair **et** sombre, et à 375px de large.

## 5. Ton rédactionnel

- Vouvoiement, phrases courtes, verbes d'action sur les boutons (« Déclarer un incident », pas « Valider »).
- Messages d'erreur : ce qui s'est passé, puis quoi faire.
- États vides : expliquer à quoi sert l'écran et proposer l'action suivante.
