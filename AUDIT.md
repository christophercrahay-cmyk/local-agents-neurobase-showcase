# Audit 02 — Génération / validation

**Question :** une réponse d'un LLM doit-elle être enregistrée telle quelle dans une base de connaissances ?

**Réponse vérifiable dans la présentation publique :** non. Neurobase décrit extraction, coercition, validation structurée et stockage. LOCAL_AGENTS distingue également orchestration, exécution et contrôle. Un schéma Pydantic ne prouve toutefois pas la véracité d'une information.

**Éléments observables :** [captures de code authentique et de consoles de tests](https://christopher-crahay.vercel.app/work/local-agents). La capture LOCAL_AGENTS concerne la suite du commit `136db6c` (266 tests réussis) et non l'arbre de travail courant. La capture NEUROBASE concerne le commit `1f515df` (105 tests réussis). Ce sont des résultats datés, pas un banc d'essai public téléchargeable.

**Limites :** les suites exécutables et les données privées ne sont pas publiées ; il n'existe pas de benchmark public reproductible sur ces pages. Les évaluations par LLM exigent un protocole et ne constituent pas une vérité absolue.

**Trace d'audit :** `02 / VALIDATION / contrat identifié`

**Étape suivante :** [03 — simulation et présentation](https://github.com/christophercrahay-cmyk/after-showcase/blob/main/AUDIT.md). Après la validation des données, comment isoler les règles du système de leur affichage ?
