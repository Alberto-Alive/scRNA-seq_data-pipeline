from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field



class QCConfig(BaseModel):
    min_genes_per_cell: int = 200
    min_cells_per_gene: int  = 3
    max_pct_mito: float = 20.0
    mito_prefix: str = "MIT-"

class PreprocessConfig(BaseModel):
    target_sum: float = 1e4
    n_top_genes: int = 2000
    hvg_flavor: Literal["seurat", "seurat_v3", "cell_ranger"] = "seurat_v3"


class IntegrateConfig(BaseModel):
    method: Literal["scvi", "harmony", "None"] = "scvi"
    batch_key: str = "batch"
    n_latent: int = 30
    max_epochs: int = 200

class ClusterConfig(BaseModel):
    n_neighbours: int= 15
    resolution: float = 1.0
    random_state: int = 0


class AnnotateConfig(BaseModel):
    seed: int = 0
    qc: QCConfig = Field(default_factory=QCConfig)
    preprocess: PreprocessConfig = Field(default_factory=PreprocessConfig)
    integrate: IntegrateConfig
