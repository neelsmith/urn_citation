import pytest

from urn_citation import Cite2Urn


class TestCite2UrnFromString:
    def test_parses_full_with_version(self):
        urn = Cite2Urn.from_string("urn:cite2:hmt:datamodels.v1:codexmodel")
        assert urn.urn_type == "cite2"
        assert urn.namespace == "hmt"
        assert urn.collection == "datamodels"
        assert urn.version == "v1"
        assert urn.object_id == "codexmodel"

    def test_parses_without_version_and_with_range_object(self):
        urn = Cite2Urn.from_string("urn:cite2:ns:coll:obj-2")
        assert urn.urn_type == "cite2"
        assert urn.namespace == "ns"
        assert urn.collection == "coll"
        assert urn.version is None
        assert urn.object_id == "obj-2"

    def test_requires_cite2_prefix(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cts:ns:coll:obj")
        assert "start with 'urn:cite2:'" in str(exc_info.value)

    def test_requires_five_colon_parts(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cite2:ns:coll")
        assert "5 colon-delimited parts" in str(exc_info.value)

    def test_collection_cannot_end_with_period(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cite2:ns:coll.:obj")
        assert "end with a period" in str(exc_info.value)

    def test_collection_allows_single_period_only(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cite2:ns:coll.v1.extra:obj")
        assert "at most one period" in str(exc_info.value)

    def test_collection_parts_must_be_non_empty(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cite2:ns:.v1:obj")
        assert "non-empty" in str(exc_info.value)

    def test_object_cannot_end_with_hyphen(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cite2:ns:coll:obj-")
        assert "end with a hyphen" in str(exc_info.value)

    def test_object_allows_single_hyphen_only(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cite2:ns:coll:one-two-three")
        assert "at most one hyphen" in str(exc_info.value)

    def test_object_parts_must_be_non_empty(self):
        with pytest.raises(ValueError) as exc_info:
            Cite2Urn.from_string("urn:cite2:ns:coll:-obj")
        assert "non-empty identifiers" in str(exc_info.value)

    def test_namespace_and_collection_and_object_required(self):
        for urn in [
            "urn:cite2::coll:obj",  # missing namespace
            "urn:cite2:ns::obj",    # missing collection
            "urn:cite2:ns:coll:",   # missing object
        ]:
            with pytest.raises(ValueError):
                Cite2Urn.from_string(urn)
