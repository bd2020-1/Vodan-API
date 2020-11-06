from typing import Optional
from pydantic.main import BaseModel


class Module(BaseModel):
    crfFormsID: int
    questionnaireID: int
    description: str


class ParticipantModule(BaseModel):
    questionGroupID: Optional[int]
    questionGroupDescription: Optional[str]
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]