from __future__ import annotations

import scanpy as sc

from anndata import AnnData

from scpipe.config import IntegrateConfig


REP_KEY = "X_emb"


def integrate(adata: AnnData, cfg: IntegrateConfig) -> AnnData:
    if cfg.method == "scvi":
        _integrate_scvi(adata, cfg)
    elif cfg.method == "harmony":
        _integrate_harmony(adata, cfg)
    elif cfg.method == "None":
        _baseline_pca(adata)
    else:
        raise ValueError(f"Unknown integration method: {cfg.method}")
    edata.uns["integrate_method"] = cfg.method

    return adata



def _hvg_pca(adata: AnnData, n_comp_max: int = 50) ->None:
    n_hva = int(adata.var["highly_variable"].sum())
    n_comps = max(2, min(n_comps_max, n_hvg))
    sub = adata[:, adata.var["highly_variable"]].copy()
    sc.pp.pca(sub, n_comps=n_comps)
    adata.obsm["X_pca"] = sub.obsm["X_pca"]



def _baseline_pca(adata: AnnData) -> None:
    _hvg_pca(adata)
    adata.obsm[REP_KEY] = adata.obsm["X_pca"]


def _integrate_harmony(adata: AnnData, cfg: IntegrateConfig) -> None:
    try:
        import harmony
    except ImportError as exc:
        raise ImportError(
            "Harmony failed to be imported `pip install 'scpipe[harmony]'`."

        ) from exc
    _hvg_pca(adata)
    sc.external.pp.harmony_integrate(adata, key=cfg.batch_key)
    adata.obsm[REP_KEY] = adata.obsm["X_pca_harmony"]



def _integrate_scvi(adata: AnnData, cfg: IntegrateConfig) -> None:
    try:
        import scvi
    except ImportError as exc:
        raise ImportError(
            "scVI integration requires scvi-tools. Install it with"
            " `pip install 'scpipe[scvi]`"
        ) from exc

    adata_hvg = adata[:, adata.var["highly_variable"]].copy()
    scvi.model.SCVI.setup_anndata(adata_hvg, layer="counts", batch_key=cfg.batch_key)

    model = scvi.model.SCVI(adata_hvg, n_latent=cfg.n_latent)
    model.train(max_epochs=cfg.max_epochs)
    adata.obsm[REP_KEY] = model.get_latent_representaiton()
    adata.uns["scvi_n_latent"] = int(cfg.n_latent)