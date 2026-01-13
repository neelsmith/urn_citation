import pytest
from pydantic import ValidationError

from urn_citation import CtsUrn


class TestCtsUrnCreation:
    """Tests for CtsUrn creation and validation."""

    def test_ctsurn_creation_with_required_fields(self):
        """Test creating a CtsUrn with required fields only."""
        urn = CtsUrn(urn_type="cts", namespace="greekLit", text_group="tlg0012")
        assert urn.urn_type == "cts"
        assert urn.namespace == "greekLit"
        assert urn.text_group == "tlg0012"
        assert urn.work is None
        assert urn.version is None
        assert urn.exemplar is None
        assert urn.passage is None

    def test_ctsurn_creation_with_all_fields(self):
        """Test creating a CtsUrn with all fields populated."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            exemplar="ex1",
            passage="1.1"
        )
        assert urn.text_group == "tlg0012"
        assert urn.work == "001"
        assert urn.version == "wacl1"
        assert urn.exemplar == "ex1"
        assert urn.passage == "1.1"

    def test_ctsurn_requires_namespace(self):
        """Test that namespace is required."""
        with pytest.raises(ValidationError) as exc_info:
            CtsUrn(urn_type="cts", text_group="tlg0012")
        assert "namespace" in str(exc_info.value)

    def test_ctsurn_requires_text_group(self):
        """Test that text_group is required."""
        with pytest.raises(ValidationError) as exc_info:
            CtsUrn(urn_type="cts", namespace="greekLit")
        assert "text_group" in str(exc_info.value)


class TestCtsUrnToString:
    """Tests for the to_string method."""

    def test_to_string_basic_urn(self):
        """Test serializing a basic CtsUrn with only required fields."""
        urn = CtsUrn(urn_type="cts", namespace="greekLit", text_group="tlg0012")
        assert urn.to_string() == "urn:cts:greekLit:tlg0012:"

    def test_to_string_with_work(self):
        """Test serializing a CtsUrn with work component."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001"
        )
        assert urn.to_string() == "urn:cts:greekLit:tlg0012.001:"

    def test_to_string_with_version(self):
        """Test serializing a CtsUrn with version component."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1"
        )
        assert urn.to_string() == "urn:cts:greekLit:tlg0012.001.wacl1:"

    def test_to_string_with_exemplar(self):
        """Test serializing a CtsUrn with exemplar component."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            exemplar="ex1"
        )
        assert urn.to_string() == "urn:cts:greekLit:tlg0012.001.wacl1.ex1:"

    def test_to_string_with_passage(self):
        """Test serializing a CtsUrn with passage component."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        assert urn.to_string() == "urn:cts:greekLit:tlg0012:1.1"

    def test_to_string_with_all_components(self):
        """Test serializing a CtsUrn with all components."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            exemplar="ex1",
            passage="1.1-1.5"
        )
        assert urn.to_string() == "urn:cts:greekLit:tlg0012.001.wacl1.ex1:1.1-1.5"


class TestCtsUrnIsRange:
    """Tests for the is_range method."""

    def test_is_range_with_range_passage(self):
        """Test is_range returns True for a range passage."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1-1.5"
        )
        assert urn.is_range() is True

    def test_is_range_with_single_passage(self):
        """Test is_range returns False for a single passage."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        assert urn.is_range() is False

    def test_is_range_with_none_passage(self):
        """Test is_range returns False when passage is None."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        assert urn.is_range() is False

    def test_is_range_with_empty_string_passage(self):
        """Test is_range returns False for empty string passage."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage=""
        )
        assert urn.is_range() is False


class TestCtsUrnRangeBegin:
    """Tests for the range_begin method."""

    def test_range_begin_with_range(self):
        """Test range_begin returns the first part of a range."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1-1.5"
        )
        assert urn.range_begin() == "1.1"

    def test_range_begin_with_single_passage(self):
        """Test range_begin returns None for a single passage."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        assert urn.range_begin() is None

    def test_range_begin_with_none_passage(self):
        """Test range_begin returns None when passage is None."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        assert urn.range_begin() is None


class TestCtsUrnRangeEnd:
    """Tests for the range_end method."""

    def test_range_end_with_range(self):
        """Test range_end returns the second part of a range."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1-1.5"
        )
        assert urn.range_end() == "1.5"

    def test_range_end_with_single_passage(self):
        """Test range_end returns None for a single passage."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        assert urn.range_end() is None

    def test_range_end_with_none_passage(self):
        """Test range_end returns None when passage is None."""
        urn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        assert urn.range_end() is None


class TestCtsUrnValidString:
    """Tests for the valid_string classmethod."""

    def test_valid_string_basic(self):
        """Test valid_string returns True for a valid basic URN."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:") is True

    def test_valid_string_with_passage(self):
        """Test valid_string returns True for a valid URN with passage."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:1.1") is True

    def test_valid_string_with_range(self):
        """Test valid_string returns True for a valid URN with range."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:1.1-1.5") is True

    def test_valid_string_with_work_hierarchy(self):
        """Test valid_string returns True for a valid URN with work hierarchy."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012.001.wacl1.ex1:1.1") is True

    def test_valid_string_too_few_components(self):
        """Test valid_string returns False for too few components."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012") is False

    def test_valid_string_too_many_components(self):
        """Test valid_string returns False for too many components."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:1.1:extra") is False

    def test_valid_string_too_many_hyphens(self):
        """Test valid_string returns False for too many hyphens in passage."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:1.1-1.5-2.1") is False

    def test_valid_string_too_many_dots(self):
        """Test valid_string returns False for too many dots in work component."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012.001.wacl1.ex1.extra:1.1") is False

    def test_valid_string_invalid_input(self):
        """Test valid_string returns False for invalid input."""
        assert CtsUrn.valid_string("") is False
        assert CtsUrn.valid_string("not:a:urn") is False

    def test_valid_string_successive_periods_in_work(self):
        """Test valid_string returns False for successive periods in work component."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012..001:") is False
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012.001..wacl1:") is False
        assert CtsUrn.valid_string("urn:cts:greekLit:..tlg0012:") is False

    def test_valid_string_successive_periods_in_passage(self):
        """Test valid_string returns False for successive periods in passage component."""
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:1..1") is False
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:1.1-1..5") is False
        assert CtsUrn.valid_string("urn:cts:greekLit:tlg0012:..1.1") is False


class TestCtsUrnFromString:
    """Tests for the from_string classmethod."""

    def test_from_string_successive_periods_in_work(self):
        """Test from_string raises ValueError for successive periods in work component."""
        with pytest.raises(ValueError) as exc_info:
            CtsUrn.from_string("urn:cts:greekLit:tlg0012..001:")
        assert "successive periods" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            CtsUrn.from_string("urn:cts:greekLit:tlg0012.001..wacl1:")
        assert "successive periods" in str(exc_info.value)

    def test_from_string_successive_periods_in_passage(self):
        """Test from_string raises ValueError for successive periods in passage component."""
        with pytest.raises(ValueError) as exc_info:
            CtsUrn.from_string("urn:cts:greekLit:tlg0012:1..1")
        assert "successive periods" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            CtsUrn.from_string("urn:cts:greekLit:tlg0012:1.1-1..5")
        assert "successive periods" in str(exc_info.value)


class TestCtsUrnWorkEquals:
    """Tests for the work_equals method."""

    def test_work_equals_identical_urns(self):
        """Test work_equals returns True for identical work hierarchies."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            exemplar="ex1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            exemplar="ex1"
        )
        assert urn1.work_equals(urn2) is True

    def test_work_equals_different_text_group(self):
        """Test work_equals returns False for different text_group."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0013"
        )
        assert urn1.work_equals(urn2) is False

    def test_work_equals_different_work(self):
        """Test work_equals returns False for different work."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="002"
        )
        assert urn1.work_equals(urn2) is False

    def test_work_equals_ignores_passage(self):
        """Test work_equals ignores passage component."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.2"
        )
        assert urn1.work_equals(urn2) is True


class TestCtsUrnWorkSimilar:
    """Tests for the work_similar method."""

    def test_work_similar_identical_urns(self):
        """Test work_similar returns True for identical work hierarchies."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001"
        )
        assert urn1.work_similar(urn2) is True

    def test_work_similar_with_none_fields(self):
        """Test work_similar returns True when non-None fields match."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1"
        )
        assert urn1.work_similar(urn2) is True

    def test_work_similar_mismatch_non_none_field(self):
        """Test work_similar returns False when non-None fields don't match."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="002"
        )
        assert urn1.work_similar(urn2) is False

    def test_work_similar_all_none_fields(self):
        """Test work_similar returns True when all fields are None."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001"
        )
        assert urn1.work_similar(urn2) is True


class TestCtsUrnPassageEquals:
    """Tests for the passage_equals method."""

    def test_passage_equals_same_passage(self):
        """Test passage_equals returns True for identical passages."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        assert urn1.passage_equals(urn2) is True

    def test_passage_equals_different_passage(self):
        """Test passage_equals returns False for different passages."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.2"
        )
        assert urn1.passage_equals(urn2) is False

    def test_passage_equals_both_none(self):
        """Test passage_equals returns True when both passages are None."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        assert urn1.passage_equals(urn2) is True


class TestCtsUrnPassageSimilar:
    """Tests for the passage_similar method."""

    def test_passage_similar_identical(self):
        """Test passage_similar returns True for identical passages."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        assert urn1.passage_similar(urn2) is True

    def test_passage_similar_refinement(self):
        """Test passage_similar returns True for refinement passages."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.11"
        )
        assert urn1.passage_similar(urn2) is True

    def test_passage_similar_no_refinement_single_char(self):
        """Test passage_similar returns False for single char without dot."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="12"
        )
        assert urn1.passage_similar(urn2) is False

    def test_passage_similar_completely_different(self):
        """Test passage_similar returns False for different passages."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            passage="2.2"
        )
        assert urn1.passage_similar(urn2) is False

    def test_passage_similar_both_none(self):
        """Test passage_similar returns True when both passages are None."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012"
        )
        assert urn1.passage_similar(urn2) is True


class TestCtsUrnUrnSimilar:
    """Tests for the urn_similar method."""

    def test_urn_similar_identical_urns(self):
        """Test urn_similar returns True for identical URNs."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            passage="1.1"
        )
        assert urn1.urn_similar(urn2) is True

    def test_urn_similar_similar_work_and_passage(self):
        """Test urn_similar returns True for similar work and passage."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            passage="1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            passage="1.11"
        )
        assert urn1.urn_similar(urn2) is True

    def test_urn_similar_different_work(self):
        """Test urn_similar returns False if work is different."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="002",
            passage="1.1"
        )
        assert urn1.urn_similar(urn2) is False

    def test_urn_similar_different_passage(self):
        """Test urn_similar returns False if passage is different."""
        urn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            passage="1.1"
        )
        urn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            passage="2.1"
        )
        assert urn1.urn_similar(urn2) is False


class TestCtsUrnRoundTrip:
    """Tests for round-trip conversion (from_string -> to_string)."""

    def test_roundtrip_basic(self):
        """Test round-trip conversion for basic URN."""
        urn_string = "urn:cts:greekLit:tlg0012:"
        urn = CtsUrn.from_string(urn_string)
        assert urn.to_string() == urn_string

    def test_roundtrip_with_work_hierarchy(self):
        """Test round-trip conversion with work hierarchy."""
        urn_string = "urn:cts:greekLit:tlg0012.001.wacl1.ex1:"
        urn = CtsUrn.from_string(urn_string)
        assert urn.to_string() == urn_string

    def test_roundtrip_with_passage(self):
        """Test round-trip conversion with passage."""
        urn_string = "urn:cts:greekLit:tlg0012:1.1-1.5"
        urn = CtsUrn.from_string(urn_string)
        assert urn.to_string() == urn_string

    def test_roundtrip_with_all_components(self):
        """Test round-trip conversion with all components."""
        urn_string = "urn:cts:greekLit:tlg0012.001.wacl1:1.1"
        urn = CtsUrn.from_string(urn_string)
        assert urn.to_string() == urn_string
