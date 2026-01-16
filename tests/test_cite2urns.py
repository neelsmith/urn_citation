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


class TestCite2UrnToString:
    def test_to_string_with_version(self):
        urn = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="datamodels",
            version="v1",
            object_id="codexmodel",
        )

        assert str(urn) == "urn:cite2:hmt:datamodels.v1:codexmodel"

    def test_to_string_without_version(self):
        urn = Cite2Urn(
            urn_type="cite2",
            namespace="ns",
            collection="coll",
            object_id="obj-2",
        )

        assert str(urn) == "urn:cite2:ns:coll:obj-2"

    def test_roundtrip_from_string_and_back(self):
        raw = "urn:cite2:hmt:datamodels.v1:codexmodel"
        urn = Cite2Urn.from_string(raw)
        assert str(urn) == raw

    def test_roundtrip_without_version(self):
        raw = "urn:cite2:ns:coll:obj"
        urn = Cite2Urn.from_string(raw)
        assert str(urn) == raw


class TestCite2UrnRangeHelpers:
    def test_is_range_true(self):
        urn = Cite2Urn.from_string("urn:cite2:ns:coll:obj-2")
        assert urn.is_range() is True

    def test_is_range_false_single_object(self):
        urn = Cite2Urn.from_string("urn:cite2:ns:coll:obj")
        assert urn.is_range() is False

    def test_range_begin_and_end(self):
        urn = Cite2Urn.from_string("urn:cite2:ns:coll:obj-2")
        assert urn.range_begin() == "obj"
        assert urn.range_end() == "2"

    def test_range_helpers_none_when_not_range(self):
        urn = Cite2Urn.from_string("urn:cite2:ns:coll:obj")
        assert urn.range_begin() is None
        assert urn.range_end() is None


class TestCite2UrnValidString:
    def test_valid_basic_and_with_version_and_range(self):
        assert Cite2Urn.valid_string("urn:cite2:ns:coll:obj") is True
        assert Cite2Urn.valid_string("urn:cite2:ns:coll.v1:obj") is True
        assert Cite2Urn.valid_string("urn:cite2:ns:coll:obj-2") is True

    def test_invalid_prefix_or_parts(self):
        assert Cite2Urn.valid_string("urn:cts:ns:coll:obj") is False
        assert Cite2Urn.valid_string("urn:cite2:ns:coll") is False

    def test_invalid_collection_rules(self):
        assert Cite2Urn.valid_string("urn:cite2:ns:coll.:obj") is False
        assert Cite2Urn.valid_string("urn:cite2:ns:coll.v1.extra:obj") is False
        assert Cite2Urn.valid_string("urn:cite2:ns:.v1:obj") is False

    def test_invalid_object_rules(self):
        assert Cite2Urn.valid_string("urn:cite2:ns:coll:obj-") is False
        assert Cite2Urn.valid_string("urn:cite2:ns:coll:one-two-three") is False
        assert Cite2Urn.valid_string("urn:cite2:ns:coll:-obj") is False

    def test_missing_namespace_collection_or_object(self):
        assert Cite2Urn.valid_string("urn:cite2::coll:obj") is False
        assert Cite2Urn.valid_string("urn:cite2:ns::obj") is False
        assert Cite2Urn.valid_string("urn:cite2:ns:coll:") is False


class TestCite2UrnCollectionEquals:
    def test_identical_collections(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj2"
        )
        assert urn1.collection_equals(urn2) is True

    def test_different_namespace(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="other",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        assert urn1.collection_equals(urn2) is False

    def test_different_collection(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="other",
            object_id="obj1"
        )
        assert urn1.collection_equals(urn2) is False

    def test_different_version(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v2",
            object_id="obj1"
        )
        assert urn1.collection_equals(urn2) is False


class TestCite2UrnCollectionContains:
    def test_identical_contains(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj2"
        )
        assert urn1.collection_contains(urn2) is True

    def test_partial_constraints_contains(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj2"
        )
        assert urn1.collection_contains(urn2) is True

    def test_namespace_mismatch_not_contained(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="other",
            collection="data",
            object_id="obj1"
        )
        assert urn1.collection_contains(urn2) is False

    def test_version_constraint_mismatch(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v2",
            object_id="obj1"
        )
        assert urn1.collection_contains(urn2) is False


class TestCite2UrnObjectEquals:
    def test_identical_objects(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="other",
            collection="other",
            object_id="obj1"
        )
        assert urn1.object_equals(urn2) is True

    def test_different_objects(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj2"
        )
        assert urn1.object_equals(urn2) is False

    def test_range_object_equality(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1-obj2"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1-obj2"
        )
        assert urn1.object_equals(urn2) is True


class TestCite2UrnDropMethods:
    def test_drop_version(self):
        urn = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        dropped = urn.drop_version()
        assert dropped.urn_type == "cite2"
        assert dropped.namespace == "hmt"
        assert dropped.collection == "data"
        assert dropped.version is None
        assert dropped.object_id == "obj1"

    def test_drop_version_already_none(self):
        urn = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        dropped = urn.drop_version()
        assert dropped.version is None
        assert dropped.object_id == "obj1"

    def test_drop_objectid(self):
        urn = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        dropped = urn.drop_objectid()
        assert dropped.urn_type == "cite2"
        assert dropped.namespace == "hmt"
        assert dropped.collection == "data"
        assert dropped.version == "v1"
        assert dropped.object_id is None

    def test_drop_objectid_already_none(self):
        urn = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data"
        )
        dropped = urn.drop_objectid()
        assert dropped.object_id is None
        assert dropped.collection == "data"

class TestCite2UrnContains:
    def test_contains_identical_urns(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        assert urn1.contains(urn2) is True

    def test_contains_partial_collection_and_equal_object(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            version="v1",
            object_id="obj1"
        )
        assert urn1.contains(urn2) is True

    def test_contains_false_different_objects(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj2"
        )
        assert urn1.contains(urn2) is False

    def test_contains_false_different_collection(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data1",
            object_id="obj1"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data2",
            object_id="obj1"
        )
        assert urn1.contains(urn2) is False

    def test_contains_requires_exact_object_match(self):
        urn1 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj"
        )
        urn2 = Cite2Urn(
            urn_type="cite2",
            namespace="hmt",
            collection="data",
            object_id="obj-sub"
        )
        # Even though collection_contains would be True,
        # contains is False because objects are not equal
        assert urn1.contains(urn2) is False