# Audit 02 — Génération / validation

**Question :** une réponse d'un LLM doit-elle être enregistrée telle quelle dans une base de connaissances ?

**Réponse vérifiable dans la présentation publique :** non. Neurobase décrit extraction, coercition, validation structurée et stockage. LOCAL_AGENTS distingue également orchestration, exécution et contrôle. Un schéma Pydantic ne prouve toutefois pas la véracité d'une information.

**Limite :** aucun jeu de tests complet ni benchmark reproductible n'est publié. Les évaluations par LLM exigent un protocole et ne constituent pas une vérité absolue.

**Trace d'audit :** `02 / VALIDATION / contrat identifié`

**Étape suivante :** [03 — simulation et présentation](https://github.com/christophercrahay-cmyk/after-showcase/blob/main/AUDIT.md). Après la validation des données, comment isoler les règles du système de leur affichage ?
