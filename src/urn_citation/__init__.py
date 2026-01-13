from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("urn_citation") # 'name' of package from pyproject.toml
except PackageNotFoundError:
    # Package is not installed (e.g., running from a local script)
    __version__ = "unknown"

from .urns import Urn, CtsUrn

__all__ = ["Urn", "CtsUrn"]