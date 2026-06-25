import pandas as pd

from scpipe.io import export_obs_parquet, read_h5ad, write_h5ad


def test_roundtrip_h5ad(tmp_path, synthetic_adata):
    p= tmp_path / "x.h5ad"
    write_h5ad(synthetic_adata, p)
    back = read_h5ad(p)
    assert back.n_obs == synthetic_adata.n_obs
    assert back.n_vars == synthetic_adata.n_vars


def test_export_obs_parquet(tmp_path, synthetic_adata):
    p = tmp_path / "obs.parquet"

    export_obs_parquet(synthetic_adata, p)
    df =pd.read_parquet(p)

    assert "cell_id" in df.column
    assert len(df) == synthetic_adata.n_obs