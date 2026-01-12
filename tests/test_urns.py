import pytest
from pydantic import ValidationError

from urn_citation import Urn, CtsUrn


class TestUrn:
    """Tests for the Urn base class."""

    def test_urn_creation_with_valid_data(self):
        """Test creating a Urn with valid data."""
        urn = Urn(urn_type="test")
        assert urn.urn_type == "test"

    def test_urn_requires_urn_type(self):
        """Test that urn_type is required."""
        with pytest.raises(ValidationError) as exc_info:
            Urn()
        assert "urn_type" in str(exc_info.value)

    def test_urn_urn_type_is_string(self):
        """Test that urn_type accepts string values."""
        urn = Urn(urn_type="custom_type")
        assert isinstance(urn.urn_type, str)
        assert urn.urn_type == "custom_type"

    def test_urn_equality(self):
        """Test that two Urns with the same urn_type are equal."""
        urn1 = Urn(urn_type="test")
        urn2 = Urn(urn_type="test")
        assert urn1 == urn2

    def test_urn_inequality(self):
        """Test that two Urns with different urn_type values are not equal."""
        urn1 = Urn(urn_type="test1")
        urn2 = Urn(urn_type="test2")
        assert urn1 != urn2

    def test_urn_model_dump(self):
        """Test that Urn can be serialized to a dictionary."""
        urn = Urn(urn_type="test")
        data = urn.model_dump()
        assert data["urn_type"] == "test"


class TestCtsUrn:
    """Tests for the CtsUrn subclass."""

    def test_ctsurn_creation_with_required_fields(self):
        """Test creating a CtsUrn with required fields."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        assert ctsurn.urn_type == "cts"
        assert ctsurn.namespace == "greekLit"
        assert ctsurn.text_group == "tlg0012"
        assert ctsurn.work is None
        assert ctsurn.version is None
        assert ctsurn.exemplar is None
        assert ctsurn.passage is None

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

    def test_ctsurn_requires_urn_type(self):
        """Test that urn_type is inherited and required."""
        with pytest.raises(ValidationError) as exc_info:
            CtsUrn(namespace="greekLit", text_group="tlg0012")
        assert "urn_type" in str(exc_info.value)

    def test_ctsurn_with_all_fields(self):
        """Test creating a CtsUrn with all fields populated."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            exemplar="ex1",
            passage="1.1-1.5",
        )
        assert ctsurn.urn_type == "cts"
        assert ctsurn.namespace == "greekLit"
        assert ctsurn.text_group == "tlg0012"
        assert ctsurn.work == "001"
        assert ctsurn.version == "wacl1"
        assert ctsurn.exemplar == "ex1"
        assert ctsurn.passage == "1.1-1.5"

    def test_ctsurn_work_is_optional(self):
        """Test that work field is optional."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        assert ctsurn.work is None

    def test_ctsurn_version_is_optional(self):
        """Test that version field is optional."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        assert ctsurn.version is None

    def test_ctsurn_exemplar_is_optional(self):
        """Test that exemplar field is optional."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        assert ctsurn.exemplar is None

    def test_ctsurn_passage_is_optional(self):
        """Test that passage field is optional."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        assert ctsurn.passage is None

    def test_ctsurn_equality_with_same_values(self):
        """Test that two CtsUrns with the same values are equal."""
        ctsurn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            passage="1.1",
        )
        ctsurn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            passage="1.1",
        )
        assert ctsurn1 == ctsurn2

    def test_ctsurn_inequality_with_different_namespace(self):
        """Test that CtsUrns with different namespace values are not equal."""
        ctsurn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        ctsurn2 = CtsUrn(
            urn_type="cts",
            namespace="latinLit",
            text_group="tlg0012",
        )
        assert ctsurn1 != ctsurn2

    def test_ctsurn_inequality_with_different_text_group(self):
        """Test that CtsUrns with different text_group values are not equal."""
        ctsurn1 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        ctsurn2 = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0013",
        )
        assert ctsurn1 != ctsurn2

    def test_ctsurn_inheritance_from_urn(self):
        """Test that CtsUrn inherits from Urn."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
        )
        assert isinstance(ctsurn, Urn)

    def test_ctsurn_model_dump(self):
        """Test that CtsUrn can be serialized to a dictionary."""
        ctsurn = CtsUrn(
            urn_type="cts",
            namespace="greekLit",
            text_group="tlg0012",
            work="001",
            version="wacl1",
            passage="1.1",
        )
        data = ctsurn.model_dump()
        assert data["urn_type"] == "cts"
        assert data["namespace"] == "greekLit"
        assert data["text_group"] == "tlg0012"
        assert data["work"] == "001"
        assert data["version"] == "wacl1"
        assert data["passage"] == "1.1"

    def test_ctsurn_model_validate(self):
        """Test that CtsUrn can be created from a dictionary using model_validate."""
        data = {
            "urn_type": "cts",
            "namespace": "greekLit",
            "text_group": "tlg0012",
            "work": "001",
            "version": "wacl1",
            "passage": "1.1",
        }
        ctsurn = CtsUrn.model_validate(data)
        assert ctsurn.urn_type == "cts"
        assert ctsurn.namespace == "greekLit"
        assert ctsurn.text_group == "tlg0012"
        assert ctsurn.work == "001"
        assert ctsurn.version == "wacl1"
        assert ctsurn.passage == "1.1"


class TestCtsUrnFromString:
    """Tests for the CtsUrn.from_string() classmethod."""

    def test_from_string_basic_urn(self):
        """Test parsing a basic CTS URN string with 5 components."""
        urn_string = "urn:cts:greekLit:tlg0012:passage"
        ctsurn = CtsUrn.from_string(urn_string)
        assert ctsurn.urn_type == "cts"
        assert ctsurn.namespace == "greekLit"
        assert ctsurn.text_group == "tlg0012"
        assert ctsurn.passage == "passage"

    def test_from_string_with_work_component(self):
        """Test parsing a CTS URN with dotted work component."""
        urn_string = "urn:cts:greekLit:tlg0012.001:passage"
        ctsurn = CtsUrn.from_string(urn_string)
        assert ctsurn.text_group == "tlg0012"
        assert ctsurn.work == "001"
        assert ctsurn.passage == "passage"

    def test_from_string_with_version_component(self):
        """Test parsing a CTS URN with version in work component."""
        urn_string = "urn:cts:greekLit:tlg0012.001.wacl1:passage"
        ctsurn = CtsUrn.from_string(urn_string)
        assert ctsurn.text_group == "tlg0012"
        assert ctsurn.work == "001"
        assert ctsurn.version == "wacl1"
        assert ctsurn.passage == "passage"

    def test_from_string_with_exemplar_component(self):
        """Test parsing a CTS URN with exemplar in work component."""
        urn_string = "urn:cts:greekLit:tlg0012.001.wacl1.ex1:passage"
        ctsurn = CtsUrn.from_string(urn_string)
        assert ctsurn.text_group == "tlg0012"
        assert ctsurn.work == "001"
        assert ctsurn.version == "wacl1"
        assert ctsurn.exemplar == "ex1"
        assert ctsurn.passage == "passage"

    def test_from_string_with_passage_range(self):
        """Test parsing a CTS URN with passage range."""
        urn_string = "urn:cts:greekLit:tlg0012:1.1-1.5"
        ctsurn = CtsUrn.from_string(urn_string)
        assert ctsurn.passage == "1.1-1.5"

    def test_from_string_with_empty_passage(self):
        """Test parsing a CTS URN with empty passage component."""
        urn_string = "urn:cts:greekLit:tlg0012:"
        ctsurn = CtsUrn.from_string(urn_string)
        assert ctsurn.passage is None

    def test_from_string_too_few_components(self):
        """Test that parsing fails with too few colon-delimited components."""
        urn_string = "urn:cts:greekLit:tlg0012"
        with pytest.raises(ValueError):
            CtsUrn.from_string(urn_string)

    def test_from_string_too_many_components(self):
        """Test that parsing fails with too many colon-delimited components."""
        urn_string = "urn:cts:greekLit:tlg0012:passage:extra"
        with pytest.raises(ValueError):
            CtsUrn.from_string(urn_string)

    def test_from_string_passage_with_too_many_hyphens(self):
        """Test that parsing fails if passage has too many hyphens."""
        urn_string = "urn:cts:greekLit:tlg0012:1.1-1.5-2.0"
        with pytest.raises(ValueError) as exc_info:
            CtsUrn.from_string(urn_string)
        assert "hyphen" in str(exc_info.value).lower()

    def test_from_string_work_component_too_many_dots(self):
        """Test that parsing fails if work component has too many dots."""
        urn_string = "urn:cts:greekLit:tlg0012.001.wacl1.ex1.extra:passage"
        with pytest.raises(ValueError) as exc_info:
            CtsUrn.from_string(urn_string)
        assert "dot-delimited" in str(exc_info.value).lower()
