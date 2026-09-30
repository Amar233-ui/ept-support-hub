# Service IA

Micro-service FastAPI **interne** (jamais exposé par Nginx), appelé uniquement par le backend avec l'en-tête `X-Internal-Token`. Le backend reste fonctionnel si ce service est indisponible (timeout 2 s, circuit breaker Resilience4j, repli sur la file manuelle).

> Statut : squelette M0 (`/health`). Les modèles arrivent au milestone M4. Ce document sera complété au fil des issues. Il sert de support pour la partie IA de la soutenance.

## Endpoints

| Endpoint | Milestone | Rôle |
|---|---|---|
| `GET /health` | M0 ✅ | vivacité |
| `POST /classify` | M4 | catégorie + service destinataire + confiance + explication |
| `POST /suggest-assignee` | M4 | classement des techniciens avec score détaillé |
| `POST /correlate` | M4 | incidents résolus similaires, même zone ou zones voisines |
| `POST /embeddings/reindex` | M4 | (ré)indexation des embeddings des tickets |
| `POST /transcribe` | M6 | audio → texte (vigiles) |

## A. Classification et routage (v1)

- **Features** : titre + description, normalisés (minuscules, accents retirés, stop-words français). TF-IDF sur mots (1-2 grammes) et caractères (3-5 grammes, robuste aux fautes de frappe).
- **Modèle** : régression logistique multinomiale (scikit-learn). La probabilité de la classe prédite sert de **confiance**.
- **Règles prioritaires** : quelques mots-clés sans ambiguïté (« fuite d'eau » → Plomberie) court-circuitent le modèle et sont signalés comme tels dans l'explication.
- **Service** : dérivé de la catégorie via la table `category → service` (configurable), pas prédit séparément.
- **Seuil** : si confiance < `AI_CLASSIFY_THRESHOLD` (0,6 par défaut), le ticket va dans la file du chef de service.
- **Explicabilité** : la réponse contient les termes qui ont le plus pesé (coefficients × TF-IDF), affichés dans l'UI.

⚠️ **Honnêteté des métriques** : le jeu d'entraînement v1 est **synthétique** (rédigé et augmenté à partir de cas réalistes de l'EPT). Précision et rappel sont mesurés sur un jeu de test tenu à l'écart (`eval/`), mais ils mesurent la cohérence du modèle avec ce jeu, **pas encore la performance sur de vrais tickets**. À présenter comme tel en soutenance.

## B. Suggestion d'assignation

Pour chaque technicien actif du service, au niveau requis (N1 par défaut) :

```
score = compétence(catégorie) × disponibilité × 1 / (1 + charge) × facteur_urgence
```

| Terme | Définition v1 |
|---|---|
| `compétence` | 1,0 si la catégorie figure dans ses compétences, 0,3 sinon |
| `disponibilité` | 1 si disponible, 0 si absent ou en congé |
| `charge` | nombre de tickets ouverts assignés, pondéré par priorité (LOW 0,5 · MEDIUM 1 · HIGH 1,5 · CRITICAL 2) |
| `facteur_urgence` | favorise les techniciens les moins chargés quand le SLA est serré |

La réponse détaille chaque terme, et l'UI les affiche (« Suggéré : A. Diop : compétent en Réseau, 2 tickets en cours »). Cette partie est calculable sans ML ; elle est testée unitairement.

## C. Corrélation et indice de récurrence

Recherche, parmi les tickets **résolus** (sur toute la période), de ceux qui ressemblent au ticket ouvert :

1. **Embedding** du ticket (titre + description) avec `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensions), stocké dans pgvector.
2. **Candidats** : les k plus proches voisins (distance cosinus, index HNSW), restreints à la zone du ticket, à ses ancêtres et à ses sœurs dans l'arbre des zones.
3. **Indice de récurrence** (entre 0 et 1, affiché en %) :

```
indice = 0,6 × similarité + 0,25 × proximité_zone + 0,15 × fréquence_récente
```

| Terme | Définition |
|---|---|
| `similarité` | similarité cosinus de l'embedding, dans [0, 1] |
| `proximité_zone` | 1 même zone · 0,7 zone sœur · 0,5 zone parente · 0,3 grand-parent |
| `fréquence_récente` | `min(1, Σ exp(−âge_jours / 90) / 3)` sur les tickets similaires de la zone : décroissance exponentielle, 3 incidents récents saturent le terme |

**Ce n'est pas une probabilité.** C'est un score heuristique, non calibré, qui sert à **ordonner et filtrer** les alertes (affichées si indice ≥ 0,5). Le code l'appelle `recurrence_index`, jamais `probability`. Une calibration (régression isotonique sur les retours « utile / pas utile » des techniciens) est une piste v2.

## D. Speech-to-text (M6)

`faster-whisper`, modèle `small`, langue `fr`, quantification int8 sur CPU. Environ 5 à 15 s pour 30 s d'audio. Le texte transcrit repasse par `/classify` ; le vigile valide titre, catégorie et zone avant création.

## Évaluation

`ai-service/eval/` contiendra un script qui affiche précision, rappel et F1 par catégorie, ainsi que la matrice de confusion, sur le jeu de test. Les résultats sont copiés ici à chaque réentraînement.
