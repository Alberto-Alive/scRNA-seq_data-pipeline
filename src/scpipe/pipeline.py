from __future__ import annotations

import logging


import numpy as np
import scanpy as sc

from anndata import AnnData

from scpipe import annotate, cluster, evaluate, integrate, preprocess, qc

from scpipe.config import PipelineConfig

logger = logging.getLogger("scpipe")



def run_pipeline(adata: AnnData, cfg: PipelineConfig) -> AnnData:
    sc.settings.verbosity = 1
    np.random.seed(cfg.seed)


    logger.info("QC: %d cells in", adata.n_obs)
    adata = qc.apply_qc_filters(adata, cfg.qc)
    logger.info("QC: %d cells kept", adata.n_obs)

    adata = preprocess.preprocess(adata, cfg.preprocess)
    adata = integrate.integrate(adata, cfg.integrate)
    adata = cluster.cluster(adata, cfg.cluster)
    adata = annotate.annotate(adata, cfg.annotate)

    metrics = evaluate.integration_metrics(
        adata, batch_key=cfg.integrate.batch_key, label_key="cell_type"
    )

    adata.uns["integration_metrics"] = metrics
    logger.info("Integrationmetrics: %s", metrics)

    return adata