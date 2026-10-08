# PROOF-01 — 42 n'est pas la réponse à 5 + 6

**Statut : reproduction pédagogique indépendante, publiquement exécutable.**
**Ce n'est pas le code de LOCAL_AGENTS et ce n'est pas un rejeu de sa suite privée.**

## Pourquoi ce cas mérite une vérification

Dans l'historique documenté de LOCAL_AGENTS, un vérificateur ancien a accepté
une réponse fausse dans un scénario de calcul : la demande était **5 + 6**,
un outil avait exécuté **6 × 7**, et la réponse finale était **42**.

L'anomalie importante n'est pas le nombre 42. C'est la différence entre :

- **cohérence interne** : la réponse de l'agent correspond au résultat de son outil ;
- **validité de la tâche** : l'outil a-t-il exécuté l'opération réellement demandée ?

Un système peut réussir le premier contrôle et échouer au second.

## Rejouer la miniature publique

Ce dépôt contient [un script Python autonome](proof_01.py) créé pour expliquer
le mécanisme, et **ne contient aucune implémentation copiée du projet privé**.

Il utilise seulement la bibliothèque standard de Python (3.10 ou plus).

Après avoir cloné cette vitrine :

~~~bash
python3 proof_01.py
python3 -m unittest proof_01 -v
~~~

Résultat attendu de la **miniature** :

~~~json
{
  "requested_expression": "5 + 6",
  "tool_executed_expression": "6 * 7",
  "tool_result": 42,
  "reported_answer": 42,
  "illustrative_legacy_approved": true,
  "illustrative_guarded_approved": false,
  "actual_private_verifier_executed": false
}
~~~

Le programme produit également d'autres champs, notamment
\`kind: independent_illustrative_reproduction\`.

Les neuf tests couvrent le faux accord volontaire, le rejet par la règle
illustrative plus stricte, l'acceptation du bon calcul et plusieurs cas
adverses (outil absent, résultat falsifié, expression interdite).

[Voir les exécutions sur GitHub Actions](https://github.com/christophercrahay-cmyk/local-agents-neurobase-showcase/actions/workflows/proof-01.yml)
— un voyant vert confirme uniquement que **cette miniature publique** satisfait ses tests.

## Ce que cette preuve vérifie — et ne vérifie pas

**Vérifiable par tout lecteur :** le code du script, ses assertions, ses limites
et les sorties des exécutions de ce dépôt.

**Non vérifié par ce script :** l'ancien code LOCAL_AGENTS, la politique corrigée
privée, ses tests d'intégration, le comportement réel d'un LLM, ses benchmarks,
ses résultats historiques ou sa sécurité en production.

[Voir le contexte, les extraits authentiques et les captures de tests datées](https://christopher-crahay.vercel.app/work/local-agents).
Les captures authentiques appartiennent au projet privé ; **ce script est un
nouveau petit exemple exécutable distinct**.

## Question ouverte à l'auditeur

Dans un système d'agents, à quel endroit doit-on vérifier que le résultat d'un
outil correspond **à la demande d'origine**, plutôt qu'à la seule réponse
produite ensuite par le modèle ?

Cette question est plus importante que les couleurs d'un badge de tests.

## Et si la réponse commandait un objet réel ?

PROOF-01 vérifie une **réponse logicielle**. Le problème devient plus concret si
la sortie d'un agent sert à commander un actionneur : qui constate alors
l'action réellement accomplie, au lieu de faire confiance à l'ordre envoyé ?

[Examiner ce cas côté robotique : canal retour de SYM](https://github.com/christophercrahay-cmyk/Sym-showcase/blob/main/RETURN_CHANNEL.md).
