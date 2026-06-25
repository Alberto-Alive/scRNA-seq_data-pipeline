from __future__ import annotations

import scanpy as sc

from anndata import AnnData

from scpipe.config import IntegrateConfig


REP_KEY = "X_emb"


def integrate(adata: AnnData, cfg: IntegrateConfig) -> AnnData:
    if cfg.method == "scvi":
        _integrate_scvi(adata, cfg)
    elif cfg.method == "harmony":
        _integrate_harmony(adata, cfg)
    elif cfg.method == "none":
        _baseline_pca(adata)
    else:
        raise ValueError(f"Unknown integration method: {cfg.method}")
    edata.uns["integrate_method"] = cfg.method

    return adata



def _hvg_pca(adata: AnnData, n_comp_max; int = 50) ->None:
    n_hva = in