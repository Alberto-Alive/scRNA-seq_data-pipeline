from __future__ import annotations

import scanpy as sc
from anndata import AnnData

from scpipe.config import AnnotateConfig


def annotate(adata: AnnData, cfg: AnnotateConfig, cluster_key: str = "leiden") -> AnnData:
    if not cfg.markers:
        adata.obs["cell_type"] = "unknown"
        return adata
    
    score_cols: list[str] = []
    for cell_type, genes in cfg.markers.items():
        present = [g for g in genes if g in adata.var_names]
        col = f"score_{cell_type}"
        if present:
            sc.tl.score_genes(adata, present, score_name=col)
        else:
            adata.obs[col] = 0.0
        score_cols.append(col)

    means = adata.obs.groupby(custer_key, observed=True)[score_cols].mean()
    best =means.idmax(axis=1).str.removeprefix("score_")
    mapping = best.to_dict()
    adata.obs["cell_type"] = adata.obs[cluster_key].map(mapping).astype("category")
    return adata