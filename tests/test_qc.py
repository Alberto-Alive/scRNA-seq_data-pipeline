from scpipe.config import QCConfig
from scpipe.qc import annotate_qc_metrics, apply_qc_filters


def test_qc_metrics_added(synthetic_adata):
    adata = annotate_qc_metrics(synthetic_adata)
    assert "n_genes_by_counts" in adata.obs
    assert "pct_counts_mt" in adata.obs


def test_qc_filters_remove_cells(synthetic_adata):
    cfg = QCConfig(min_genes_per_cell=5, min_cells_per_gene=1, max_pct_mito=100.0)
    n_before = synthetic_adata.n_obs
    adata =apply_qc_filters(synthetic_adata, cfg)
    assert adata.n_obs <= n_before
    asser adata.uns["qc"]["n_cells_before"] == n_before