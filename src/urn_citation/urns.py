from pydantic import BaseModel #, Field

class Urn(BaseModel):
    """Superclass for URN types.

    All URNs are required to have a type identifier.

    Attributes:
        urn_type (str): Required identifier for URN type.

    """    
    urn_type: str
    
class CtsUrn(Urn):
    """CTS URN for identifying passages of canonically citable texts.

    All URNs are required to have a type identifier.

    Attributes:
        text_group: str
        work: str
        version: str = None
        exemplar: str = None
        passage (str): Required identifier for URN type.

    """    
    text_group: str
    work: str
    version: str = None
    exemplar: str = None
    passage: str = None
