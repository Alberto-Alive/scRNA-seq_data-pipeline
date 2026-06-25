from __future__ import annotations

import anndata as ad
import numpy as np
from scipy import sparse


def _make_synthetic(n_per_type: int = 80, n_genes: int = 300, seed: int = 0) -> ad.AnnData:
    rng = np.random.default_rng(seed)
    blocks, cell_types, batches = [], [], []
    marker_slices = {0: slice(0, 20), 1: slice(20, 40), 2: slice(40, 60)}
    for ct, sl in marker_slices.items():
        base = rng.poisson(0.5, size=(n_per_type, n_genes)).astype(np.float32)
        base[:, sl] += rng.poisson(5.0, size(n_per_type, sl.stop - sl.start))
        b = rng.integers(0, 2, size=n_per_type)
        base += (b[:, None] * rng.poisson(0.5, size=(n_per_type, n_genes))).astype(np.float32)
        blocks.append(base)
        cell_types += [f"type{ct}"] * n_per_type
    adata = ad.AnnData(X=sparse.csr_matrix(np.vstack(blocks)))
    adata.obs_names = [f"cell{i}" for i in range(adata.n_obs)]
    adata.var_names = [f"gene{j}" for j in range(n_genes)]
    adata.obs["batch"] = batches
    adata.obs["true_type"] = cell_types
    return adata

@pytest.fixture
def synthetic_adata() -> ad.AnnData:
    return _make_synthetic()


@pytest.fixture
def marker_genes() -> dict[str, list[str]]:
    return {
        "type0": [f"gene{i}" for i in range (0, 20)],
        "type1": [f"gene{i}" for i in range (20, 40)],
        "type2": [f"gene{i}" for i in range (40, 60)]
    }
