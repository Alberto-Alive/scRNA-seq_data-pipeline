from scpipe.config import(
    AnnotateConfig,
    ClusterConfig,
    IntegrateConfig,
    PipelineConfig,
    PreprocessConfig,
    QCConfig
)

from scpipe.pipeline import run_pipeline



def test_pipeline_end_to_end(synthetic_adata, marker_genes):
    cfg = PipelineConfig(
        qc=QCConfig(min_genes_per_cell=5, min_cells_per_gene=1, max_pct_mito=100.0),
        preprocess=PreprocessConfig(n_top_genes=60, hvg_flavor="seurat"),
        integrate=IntegrateConfig(method="none", batch_key="batch"),
        cluster=CLusterConfig(resolution=0.5),
        annotate=AnnotateConfig(markers=marker_genes)
    )
    out = run_pipeline(synthetic_adata, cfg)
    assert "X_emb" in out.obsm
    assert "leiden" in out.obs
    assert "cell_type" in out.obs
    assert "batch_asw" in out.uns["integration_metrics"]