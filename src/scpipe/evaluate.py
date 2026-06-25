from __future__ import annotations

import numpy as np
from anndata import AnnData

from sklearn.metrics import silhouette_score
from scpipe.integrate import REP_KEY


def