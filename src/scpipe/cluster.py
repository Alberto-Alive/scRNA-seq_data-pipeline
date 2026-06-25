from __future__ import annotations


import scanpy as sc

from anndata import AnnData

from scpipe.config import ClusterConfig
from scpipe.integrate import REP_KEY


def cluster(adata: AnnData, cfg: ClusterConfig ) -> AnnData:
    rep = REP_KEY if 