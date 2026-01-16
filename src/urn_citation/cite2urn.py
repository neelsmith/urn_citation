from pydantic import model_validator
from .urn import Urn

# Example CITE2URN
#urn:cite2:hmt:datamodels.v1:codexmodel


class Cite2Urn(Urn):
    """
    A class representing a CITE2URN, which is a specific type of URN used in the CITE architecture.
    """
    namespace: str
    collection: str
    version: str | None = None
    object_id: str | None = None

    @classmethod
    def from_string(cls, raw_string: str) -> "Cite2Urn":
        """Parse a ``urn:cite2`` string into a ``Cite2Urn`` instance.

        The string must be in the form ``urn:cite2:<namespace>:<collection[.version]>:<object[-range]>``.
        """
        if not raw_string.startswith("urn:cite2:"):
            raise ValueError("CITE2 URN must start with 'urn:cite2:'")

        parts = raw_string.split(":")
        if len(parts) != 5:
            raise ValueError(
                f"CITE2 URN must have 5 colon-delimited parts, got {len(parts)} from {raw_string}."
            )

        header, urn_type, namespace, collection_info, object_info = parts

        if header != "urn":
            raise ValueError("CITE2 URN must start with 'urn'")
        if urn_type != "cite2":
            raise ValueError("CITE2 URN must include the cite2 type identifier")

        if not namespace:
            raise ValueError("Namespace component cannot be empty")
        if not collection_info:
            raise ValueError("Collection info component cannot be empty")
        if not object_info:
            raise ValueError("Object component cannot be empty")

        if collection_info.endswith("."):
            raise ValueError("Collection info cannot end with a period")
        collection_parts = collection_info.split(".")
        if len(collection_parts) > 2:
            raise ValueError("Collection info can contain at most one period to separate collection and version")
        if any(part == "" for part in collection_parts):
            raise ValueError("Collection info must contain non-empty collection/version values")

        collection = collection_parts[0]
        version = collection_parts[1] if len(collection_parts) == 2 else None

        if object_info.endswith("-"):
            raise ValueError("Object component cannot end with a hyphen")
        object_parts = object_info.split("-")
        if len(object_parts) > 2:
            raise ValueError("Object component can contain at most one hyphen to indicate a range")
        if any(part == "" for part in object_parts):
            raise ValueError("Object component must contain non-empty identifiers")

        object_id = object_info

        return cls(
            urn_type=urn_type,
            namespace=namespace,
            collection=collection,
            version=version,
            object_id=object_id,
        )
