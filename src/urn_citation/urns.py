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
        

# Functions for 0.1 release:
#
# - isrange
# - get_range_end, get_range_start
# - valid_urn_string



