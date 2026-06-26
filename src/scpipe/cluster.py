from __future__ import annotations


import scanpy as sc

from anndata import AnnData

from scpipe.config import ClusterConfig
from scpipe.integrate import REP_KEY


def cluster(adata: AnnData, cfg: ClusterConfig ) -> AnnData:
    rep = REP_KEY if REP_KEY in adata.obsm else "X_pca"
    sc.pp.neighbors(adata, n_neighbors=cfg.n_neighbours, use_rep=rep, random_state=cfg.random_state)
    sc.tl.leiden(
        adata,
        resolution=cfg.resolution,
        random_state=cfg.random_state,
        flavor="igraph",
        n_iterations=2,
        directed=False
    )

    sc.tl.umap(adata, random_state=cfg.random_state)
    return adata