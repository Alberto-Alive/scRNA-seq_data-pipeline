from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("scpipe")
except PackageNotFoundError:
    __version__ = "0.0.0"

from scpipe.config import PipelineConfig

__all__ = ["PipelineConfig", "__version__"]