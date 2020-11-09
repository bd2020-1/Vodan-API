from typing import Optional, List

from pydantic import BaseModel
from models.listvalues import ListValue


class Question(BaseModel):
    questionID: int
    questionOrder: int
    description: str
    questionTypeID: int  = None
    listTypeID: Optional[int] = None
    ListValues: List[ListValue] = None
    questionGroupID: int = None
    subordinateTo: Optional[int] = None
    isAbout: Optional[int] = None
