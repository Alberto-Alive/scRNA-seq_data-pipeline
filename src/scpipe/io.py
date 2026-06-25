def read_h5ad(path: str | Path, backend: bool = False):
    return ad.read_h5ad(path, backed="r" if backend else None)


def write_h5ad(adata: ad.AnnData, path: str | Path, compression: str = "gzip"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(path, compression=compression)


def export_obs_parquet(adata: ad.AnnData, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df = adata.obs.copy()
    df.index.name = "cell_id"
    df.reset_index().to_parquet(path, index=False)
