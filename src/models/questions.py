from typing import Optional

from pydantic import BaseModel


class Question(BaseModel):
    questionID: int
    description: str
    questionTypeID: int
    listTypeID: Optional[int] = None
    questionGroupID: int = None
    subordinateTo: Optional[int] = None
    isAbout: Optional[int] = None
