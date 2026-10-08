# Code examples — LOCAL_AGENTS + Neurobase

> **Exemples illustratifs et simplifiés**, non extraits certifiés des dépôts privés. Ils rendent les idées vérifiables à la lecture, pas leurs performances réelles.

## Validation structurée avant stockage

```python
from pydantic import BaseModel, Field, ConfigDict, ValidationError

class MemoryFact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_id: str = Field(min_length=1)
    statement: str = Field(min_length=1, max_length=2000)
    confidence: float = Field(ge=0.0, le=1.0)

def parse_candidate(payload: dict) -> MemoryFact | None:
    try:
        return MemoryFact.model_validate(payload)
    except ValidationError:
        return None
```

La validation du schéma garantit un **format**, pas la vérité du fait : vérification de source, autorisation et politique de conservation restent nécessaires.

## Fusion de résultats lexicaux et sémantiques

```python
from collections import defaultdict

def reciprocal_rank_fusion(
    ranked_lists: list[list[str]], k: int = 60
) -> list[tuple[str, float]]:
    if k <= 0:
        raise ValueError("k must be positive")

    scores = defaultdict(float)
    for results in ranked_lists:
        for rank, doc_id in enumerate(dict.fromkeys(results), start=1):
            scores[doc_id] += 1.0 / (k + rank)

    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))
```

**Point d'architecture :** FTS5 et la recherche vectorielle peuvent proposer des classements distincts, fusionnés ici sans supposer que leurs scores bruts sont comparables. Les métriques de pertinence, les permissions documentaires et les performances doivent être mesurées séparément.
