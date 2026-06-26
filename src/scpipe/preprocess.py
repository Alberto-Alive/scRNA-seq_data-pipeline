from __future__ import annotations

import logging

import scanpy as sc

from anndata import AnnData

from scpipe.config import PreprocessConfig

logger = logging.getLogger("scpipe")

"""
The purpose of this preprocess() function is to 
prepare the raw single-cell data so it is usable 
for PCA, integration, clustering, and annotation.
"""
def preprocess(adata: AnnData, cfg: PreprocessConfig) -> AnnData:
    adata.layers["counts"] = adata.X.copy()

    flavor = cfg.hvg_flavor
    if flavor == "seurat_v3":
        try:
            import skmisc
        except ImportError:
            logger.warning(
                 "scikit-misc not installed; falling back to 'seurat' HVG flavour. "
                "Install scpipe[scvi] to enable seurat_v3."
            )
            flavor = "seurat"

        if flavor == "seurat_v3":
            sc.pp.highly_variable_genes(
                adata, n_top_genes=cfg.n_top_genes, flavor="seurat_v3", layer="counts"
            )
            sc.pp.normalize_total(adata, target_sum=cfg.target_sum)
            sc.pp.log1p(adata)
        else:
            sc.pp.normalize_total(adata, target_sum=cfg.target_sum)
            sc.pp.log1p(adata)
            sc.pp.highly_variable_genes(adata, n_top_genes=cfg.n_top_genes, flavor=flavor)
        adata.raw = adata
        return adata