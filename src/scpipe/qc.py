from __future__ import annotations

import scanpy as sc

from anndata import AnnData

from scpipe.config import QCConfig


def annotate_qc_metrics(adata: AnnData,  mito_prefix: str = "MT-") -> AnnData:
    adata.var["mt"] = adata.var_names.str.upper().str.startswith(mito_prefix.upper())
    sc.pp.claculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)
    return adata