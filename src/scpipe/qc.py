from __future__ import annotations

import scanpy as sc

from anndata import AnnData

from scpipe.config import QCConfig


def annotate_qc_metrics(adata: AnnData,  mito_prefix: str = "MT-") -> AnnData:
    adata.var["mt"] = adata.var_names.str.upper().str.startswith(mito_prefix.upper())
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)
    return adata


def apply_qc_filters(adata: AnnData, cfg: QCConfig) -> AnnData:
    adata = annotate_qc_metrics(adata, mito_prefix=cfg.mito_prefix)
    n_start = adata.n_obs

    sc.pp.filter_cells(adata, min_genes=cfg.min_genes_per_cell)
    sc.pp.filter_genes(adata, min_cells=cfg.min_cells_per_gene)
    adata = adata[adata.obs["pct_count_mt"] <= cfg.max_pct_mito].copy()

    adata.uns["qc"]= {
        "n_cells_before": int(n_start),
        "n_cells_after": int(adata.n_obs),
        "max_pct_mito": float(cfg.max_pct_mito)
    }

    return adata