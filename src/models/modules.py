from typing import Optional
from pydantic.main import BaseModel


class ParticipantModule(BaseModel):
    questionGroupID: Optional[int]
    questionGroupDescription: Optional[str]
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]


class ParticipantModuleGroup(BaseModel):
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
