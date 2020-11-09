from typing import Optional, List

from pydantic import BaseModel
from models.listvalues import ListValue


class Answer(BaseModel):
    questionID: int
    listOfValuesID: Optional[int] = None
    answer: Optional[str] = None
