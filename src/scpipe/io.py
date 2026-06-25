def read_h5ad(path: str | Path, backend: bool = False):
    return ad.read_h5ad(path, backed="r" if backend else None)


def write_h5ad(adata: ad.AnnData, path: str | Path, compression: str = "gzip"):
    Path(path).parent.mkdir

def export_obs_parquet():
