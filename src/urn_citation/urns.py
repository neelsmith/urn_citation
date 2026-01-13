from pydantic import BaseModel #, Field

class Urn(BaseModel):
    """Superclass for URN types.

    All URNs are required to have a type identifier.

    Attributes:
        urn_type (str): Required identifier for URN type.

    """    
    urn_type: str
    
class CtsUrn(Urn):
    """A CTS URN identifying a passage of a canonically citable text.

    Canonical Text Service (CTS) URNs model passages of texts with two overlapping hierarchies: a work hierarchy, and a passage hierarchy. Values in the work hierarchy belong to a specified namespace. The work hierarchy is required to identify at least a text group; optionally, it may specify a work, a version (edition or translation) of the work, and exemplar (specific copy of the version). The passage hierarchy may be empty, in which case the URN refers to the entire contents of the work identified in the work hierarchy. Otherwise, the passage hierarchy identifies a specific passage of the work, at any depth of the citation hierarchy appropriate for the work    (e.g., book, chapter, verse, line, token.) The passage hierarchy may identify either a single passage or a range of passages.

    Attributes:
        namespace (str): Required identifier for the namespace of the text (e.g., "greekLit" or "latinLit") where values for the work hierarchy are defined.
        text_group (str): Required identifier for text group.
        work (str): Optional identifier for work.
        version(str): Optional identifier for version (edition or translation) of the work.
        exemplar(str): Optional identifier for exemplar (specific copy of the version) of the work.
        passage (str): Optional identifier for passage of the work, at any depth of the citation hierarchy appropriate for the work (e.g., book, chapter, verse, line, token). May identify either a single passage or a range of passages.
    """    
    namespace: str
    text_group: str
    work: str | None = None
    version: str | None = None
    exemplar: str | None = None
    passage: str | None = None

    @classmethod
    def from_string(cls, raw_string):
        # 1. Split the string into a list of values
        parts = raw_string.split(":")
        if len(parts) != 5:
            raise ValueError("Bad.")
        header, urn_type, namespace, work_component, passage_component = parts

        rangeparts = passage_component.split("-")
        if len(rangeparts) > 2:
            raise ValueError(f"Passage component of CTS URN cannot have more than one hyphen to indicate a range, found {len(rangeparts)-1} hyphenated parts in {passage_component}.")
        
        if ".." in work_component:
            raise ValueError(f"Work component of CTS URN cannot contain successive periods, found in {work_component}.")
        
        if ".." in passage_component:
            raise ValueError(f"Passage component of CTS URN cannot contain successive periods, found in {passage_component}.")
        
        workparts = work_component.split(".")
        if len(workparts) > 4:
            raise ValueError(f"Work component of CTS URN cannot have more than 4 dot-delimited components, got {len(workparts)} from {work_component}.")

        groupid, workid, versionid, exemplarid =         (workparts + [None] * 4)[:4]
     
        if not passage_component:
            passage_component = None

        return cls(
            urn_type=urn_type,
            namespace=namespace,
            text_group=groupid,
            work=workid,
            version=versionid,
            exemplar=exemplarid,
            passage=passage_component
        )

    def to_string(self) -> str:
        """Serialize the CtsUrn to its string representation.
        
        Returns a CTS URN string in the format:
        urn:cts:namespace:work.hierarchy:passage
        
        Where work.hierarchy is constructed from the text_group, work, version, and exemplar,
        and passage is the passage component (or empty string if None).
        
        Returns:
            str: The serialized CTS URN string.
        """
        # Build the work component from the work hierarchy
        work_parts = [self.text_group]
        if self.work is not None:
            work_parts.append(self.work)
        if self.version is not None:
            work_parts.append(self.version)
        if self.exemplar is not None:
            work_parts.append(self.exemplar)
        
        work_component = ".".join(work_parts)
        
        # Build the passage component (empty string if None)
        passage_component = self.passage if self.passage is not None else ""
        
        # Construct the full URN string
        return f"urn:{self.urn_type}:{self.namespace}:{work_component}:{passage_component}"

    def is_range(self) -> bool:
        """Check if the passage component represents a range.
        
        A passage is a range if it contains exactly one hyphen, indicating both
        a range beginning and range end separated by that hyphen.
        
        Returns:
            bool: True if the passage is a range, False otherwise.
        """
        if self.passage is None:
            return False
        
        range_parts = self.passage.split("-")
        return len(range_parts) == 2

    def range_begin(self) -> str | None:
        """Get the beginning of a passage range.
        
        Returns the first range piece if the passage component represents a range
        (i.e., contains exactly one hyphen). Returns None if the passage is not
        a range or if passage is None.
        
        Returns:
            str | None: The beginning of the range, or None if not a range.
        """
        if not self.is_range():
            return None
        
        range_parts = self.passage.split("-")
        return range_parts[0]

    def range_end(self) -> str | None:
        """Get the end of a passage range.
        
        Returns the second range piece if the passage component represents a range
        (i.e., contains exactly one hyphen). Returns None if the passage is not
        a range or if passage is None.
        
        Returns:
            str | None: The end of the range, or None if not a range.
        """
        if not self.is_range():
            return None
        
        range_parts = self.passage.split("-")
        return range_parts[1]

    @classmethod
    def valid_string(cls, raw_string: str) -> bool:
        """Check if a string is valid for constructing a CtsUrn.
        
        A valid CTS URN string must:
        - Split into exactly 5 colon-delimited components
        - Have a passage component with at most 1 hyphen (for ranges)
        - Have a work component with at most 4 dot-delimited parts
        
        Args:
            raw_string (str): The string to validate.
        
        Returns:
            bool: True if the string is valid, False otherwise.
        """
        try:
            parts = raw_string.split(":")
            if len(parts) != 5:
                return False
            
            header, urn_type, namespace, work_component, passage_component = parts
            
            # Check passage component (at most 1 hyphen)
            rangeparts = passage_component.split("-")
            if len(rangeparts) > 2:
                return False
            
            # Check for successive periods in work and passage components
            if ".." in work_component or ".." in passage_component:
                return False
            
            # Check work component (at most 4 dot-delimited parts)
            workparts = work_component.split(".")
            if len(workparts) > 4:
                return False
            
            return True
        except Exception:
            return False

    def work_equals(self, other: "CtsUrn") -> bool:
        """Check if the work hierarchy is equal to another CtsUrn.
        
        Compares the text_group, work, version, and exemplar fields.
        
        Args:
            other (CtsUrn): The CtsUrn to compare with.
        
        Returns:
            bool: True if all work hierarchy fields are equal, False otherwise.
        """
        return (
            self.text_group == other.text_group
            and self.work == other.work
            and self.version == other.version
            and self.exemplar == other.exemplar
        )


    # rewrite this using a more elegant `getattr` approach, and also add a docstring
    def work_similar(self, other: "CtsUrn") -> bool:
        """Check if the work hierarchy is similar to another CtsUrn.
        
        Returns True if all non-None values of text_group, work, version, and exemplar
        in this CtsUrn equal the corresponding values in the other CtsUrn.
        
        Args:
            other (CtsUrn): The CtsUrn to compare with.
        
        Returns:
            bool: True if all non-None work hierarchy fields match, False otherwise.
        """
        if self.text_group is not None and self.text_group != other.text_group:
            return False
        if self.work is not None and self.work != other.work:
            return False
        if self.version is not None and self.version != other.version:
            return False
        if self.exemplar is not None and self.exemplar != other.exemplar:
            return False
        return True

    def passage_equals(self, other: "CtsUrn") -> bool:
        """Check if the passage component is equal to another CtsUrn.
        
        Compares the passage field of this CtsUrn with the passage field of another.
        
        Args:
            other (CtsUrn): The CtsUrn to compare with.
        
        Returns:
            bool: True if the passage fields are equal, False otherwise.
        """
        return self.passage == other.passage

    def passage_similar(self, other: "CtsUrn") -> bool:
        """Check if the passage component is similar to another CtsUrn.
        
        Returns True if:
        - The passages are exactly equal, OR
        - The other passage is at least 2 characters longer and starts with 
          this passage followed by a period character.
        
        Examples:
        - passage="1", other.passage="1.11" -> True
        - passage="1", other.passage="12" -> False
        
        Args:
            other (CtsUrn): The CtsUrn to compare with.
        
        Returns:
            bool: True if the passages match the similarity criteria, False otherwise.
        """
        # Check exact equality
        if self.passage == other.passage:
            return True
        
        # Check if other passage is a refinement of this passage
        if self.passage is not None and other.passage is not None:
            expected_prefix = self.passage + "."
            return (
                len(other.passage) >= len(self.passage) + 2
                and other.passage.startswith(expected_prefix)
            )
        
        return False

    def urn_similar(self, other: "CtsUrn") -> bool:
        """Check if this CtsUrn is similar to another CtsUrn.
        
        Returns True if both the work hierarchy and passage are similar.
        
        Args:
            other (CtsUrn): The CtsUrn to compare with.
        
        Returns:
            bool: True if both work_similar and passage_similar are True, False otherwise.
        """
        return self.work_similar(other) and self.passage_similar(other)

        



