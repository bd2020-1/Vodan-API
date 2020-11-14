from typing import Optional

from pydantic import BaseModel


class Answer(BaseModel):
    questionID: int
    listOfValuesID: Optional[int] = None
    answer: Optional[str] = None
