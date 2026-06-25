import numpy as np

from scpipe.config import PreprocessConfig

from scpipe.preprocess import preprocess



def test_preprocess_selects_hvgs_and_keeps_counts(synthetic_adata):
    cfg = PreprocessConfig(n_top_genes=50, hvg_flavor="seurat")
    adata = preprocess(synthetic_adata, cfg)
    assert "counts" in adata.layers
    assert "higly_variable" in adata.var
    n_hvg = int(adata.var["highly_variable"].sum())
    assert 0 < n_hvg <= 50
    assert float(np.asarray(adata.X.max())) < float