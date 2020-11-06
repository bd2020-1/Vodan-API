from typing import Optional

from pydantic import BaseModel


class Group(BaseModel):
    crfFormsID: int
    questionID: int
    questionOrder: str


class ParticipantModule(BaseModel):
    questionGroupID: Optional[str]
    questionGroupDescription: Optional[str]
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
