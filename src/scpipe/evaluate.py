from __future__ import annotations

import numpy as np
from anndata import AnnData

from sklearn.metrics import silhouette_score
from scpipe.integrate import REP_KEY


def _safe_silhouette(emb: np.ndarray, labels) -> float:
    labels = np.asarray(labels)
    if len(set(labels.tolist())) < 2:
        return float("nan")
    return float(silhouette_score(emb, labels))


def integration_metrics(
    adata: AnnData, batch_key: str = "batch", label_key: str | None = "cell_type"
) -> dict[str, float]:
    emb = adata.obsm[REP_KEY]
    metrics: dict[str, float] = {}
    if batch_key in adata.obs:
        metrics["batch_asw"] = _safe_silhouette(emb, adata.obs[batch_key])
    if label_key and label_key in adata.obs:
        metrics["bio_asw"] = _safe_silhouette(emb, adata.obs[label_key])
    return metrics