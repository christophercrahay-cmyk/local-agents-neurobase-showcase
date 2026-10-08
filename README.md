# LOCAL_AGENTS + Neurobase

> Expérimentations autour d'agents IA orchestrés et d'une base de connaissances locale : exécution, mémoire, recherche hybride et évaluation.

**Statut : vitrine technique.** Les dépôts de développement restent privés. Cette présentation décrit les composants et les choix d'architecture à un niveau permettant de comprendre le travail sans publier les implémentations propriétaires, données, prompts ou configurations internes.

> **Technical review:** [Architecture evidence and limitations](AUDIT.md) — model output, validation and persistence.

**[Voir les extraits de code authentique et les consoles de tests sur le portfolio](https://christopher-crahay.vercel.app/work/local-agents)** — quatre captures de code réel, tests LOCAL_AGENTS sur le seul commit `136db6c` (266 réussis) et NEUROBASE sur `1f515df` (105 réussis). Les résultats ne valident ni l'arbre de travail en cours ni les systèmes privés dans leur ensemble.

## Exemples de code commentés

[Consulter les exemples techniques](CODE_EXAMPLES.md) — extraits **illustratifs**, volontairement simplifiés, distincts du code privé. Ils montrent des frontières d'architecture et leurs limites, sans prétendre constituer une preuve de fonctionnement.


## Deux projets complémentaires

**LOCAL_AGENTS** explore l'orchestration de plusieurs agents spécialisés autour d'une mission : routage, délégation, contrôle, mémoire et exécution.

**Neurobase** explore la construction d'une mémoire technique structurée : extraction, validation, stockage et recherche lexicale + sémantique.

Ensemble, ils abordent une question commune :

> Comment construire un système IA qui ne se limite pas à un prompt isolé, mais dispose d'une architecture d'exécution, d'une mémoire exploitable et de mécanismes d'évaluation ?

## Vue d'ensemble

```text
                    Mission utilisateur
                           |
                           v
                  ┌──────────────────┐
                  │ Routage / pilotage│
                  └────────┬─────────┘
                           |
                ┌──────────┴──────────┐
                v                     v
        Agents spécialisés      Mémoire / RAG
                |                     |
                v                     v
        Exécution / outils     Recherche hybride
                |              lexicale + vecteur
                └──────────┬──────────┘
                           v
                    Contrôle qualité
                           |
                           v
                       Résultat
```

Ce diagramme est volontairement simplifié.

# LOCAL_AGENTS

## Orchestration

Le prototype organise les responsabilités en plusieurs niveaux d'agents. L'intérêt n'est pas le vocabulaire utilisé pour ces rôles, mais la séparation explicite entre :

- réception et routage d'une mission ;
- découpage en sous-tâches ;
- exécution spécialisée ;
- contrôle et éventuelle reprise.

Certaines contraintes de communication sont imposées par l'orchestrateur lui-même plutôt que laissées uniquement aux instructions textuelles des modèles.

## Routage

Toutes les missions ne nécessitent pas la même quantité de calcul.

Le système peut distinguer une demande simple, traitable avec un chemin court, d'une mission nécessitant davantage d'orchestration.

```text
Mission
  |
  +-- simple ------> chemin court
  |
  +-- complexe ----> décomposition
                       |
                       +--> agents spécialisés
                       |
                       +--> contrôle
                       |
                       +--> synthèse
```

## API et exécution

Le projet comprend une couche de service autour de **Python / FastAPI**, avec notamment :

- soumission asynchrone de missions ;
- persistance des jobs ;
- file d'exécution ;
- suivi de l'état d'une mission ;
- garde-fous pour l'accès distant ;
- interface web expérimentale.

Une contrainte importante vient du matériel : plusieurs requêtes ne doivent pas nécessairement déclencher simultanément plusieurs inférences concurrentes sur le même GPU. L'orchestration doit donc également gérer les ressources, pas seulement les messages entre agents.

## IA locale et services externes

L'architecture a été expérimentée avec des modèles locaux via **Ollama**, tout en gardant des connecteurs permettant de comparer ou d'utiliser d'autres fournisseurs dans certains scénarios.

Cela permet d'explorer concrètement les compromis entre :

- confidentialité ;
- latence ;
- coût ;
- capacité des modèles ;
- ressources GPU disponibles.

La présence de connecteurs cloud ne signifie donc pas que l'ensemble du système est « 100 % local ».

## Évaluation

Le projet possède des suites d'évaluation permettant de rejouer des cas et de faire examiner les réponses selon des critères définis.

Un juge peut lui-même être un modèle, ce qui impose une précaution importante : **une note produite par un LLM n'est pas une vérité terrain**.

Les résultats expérimentaux sont donc traités comme des mesures datées utiles pour comparer des versions, pas comme une garantie générale de performance.

# Neurobase

## Objectif

Neurobase transforme des sources en fiches structurées et interroge ensuite cette connaissance par plusieurs méthodes complémentaires.

```text
Sources
   ↓
Extraction
   ↓
Coercition / normalisation
   ↓
Validation structurée
   ↓
SQLite
   ├── index lexical
   └── index vectoriel
          ↓
   Recherche hybride
```

## Validation avant stockage

Une sortie produite par un modèle n'est pas considérée automatiquement comme une donnée valide.

Le pipeline introduit une étape de validation structurée avec **Pydantic** avant l'import dans la base. Cette séparation entre génération probabiliste et contrat de données déterministe est un principe important du projet.

## Recherche lexicale + sémantique

La mémoire combine :

- **SQLite FTS5** pour la recherche lexicale ;
- des **embeddings** pour la proximité sémantique ;
- un index vectoriel local ;
- une fusion pondérée des signaux.

L'objectif est d'éviter de dépendre exclusivement d'une recherche par mots exacts ou, à l'inverse, exclusivement d'une similarité vectorielle.

Les coefficients exacts et les mécanismes internes peuvent évoluer au fil des expérimentations ; cette vitrine ne constitue pas la spécification du moteur privé.

## Embeddings

Neurobase a notamment été expérimenté avec un modèle d'embeddings multilingue exécuté localement. La génération des vecteurs peut ainsi être découplée du fournisseur utilisé pour d'autres tâches de traitement de texte.

# Boucle mémoire expérimentale

LOCAL_AGENTS explore également une consolidation différée de certaines missions : revisiter des interactions passées, extraire des apprentissages candidats, les faire contrôler puis ne conserver que ce qui satisfait les critères définis.

```text
Historique
   ↓
Extraction d'un apprentissage candidat
   ↓
Validation / contrôle
   ↓
Accepté ? ── non → rejet
   |
  oui
   ↓
Base de connaissances
```

Il ne s'agit pas d'un entraînement du modèle : c'est une **mise à jour contrôlée de la mémoire externe**.

# Stack publique

| Domaine | Technologies / approches |
| --- | --- |
| Langage | Python |
| API | FastAPI |
| Validation | Pydantic |
| Modèles locaux | Ollama |
| Persistance | SQLite |
| Recherche lexicale | FTS5 |
| Recherche sémantique | embeddings + index vectoriel |
| Orchestration | agents spécialisés + bus |
| Évaluation | suites de cas + juge configurable |
| Interface | cockpit web expérimental |

# Ce que ces projets démontrent

Ces prototypes couvrent plusieurs problèmes rencontrés lorsqu'on passe d'un appel LLM à un **système IA** :

1. décider quel composant doit traiter une demande ;
2. faire respecter des contrats entre composants ;
3. gérer les ressources d'inférence ;
4. conserver et rechercher de la connaissance ;
5. séparer sorties probabilistes et données validées ;
6. mesurer les changements avec des évaluations reproductibles ;
7. exposer le système par une API et une interface utilisables.

C'est cette couche d'intégration qui correspond à mon positionnement d'**AI Builder / intégrateur de systèmes IA**.

## Ce qui reste privé

Cette vitrine ne publie pas :

- les dépôts sources de LOCAL_AGENTS ou Neurobase ;
- les prompts et instructions internes ;
- les jeux d'évaluation privés ;
- les données de connaissance ;
- les configurations d'agents ;
- les clés et variables d'environnement ;
- les détails permettant de reproduire les mécanismes propriétaires ;
- les documents internes d'audit.

Les métriques historiques ne sont volontairement pas mises en avant ici sans leur protocole complet et leur contexte d'exécution.

---

**Christopher Crahay**  
AI Builder — Intégrateur de systèmes IA


<!-- audit-sequence: 02 | claims require evaluation; evaluation requires context -->
