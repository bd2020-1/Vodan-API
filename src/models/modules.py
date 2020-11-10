from typing import Optional
from pydantic.main import BaseModel


class ParticipantModuleAnswer(BaseModel):
    questionGroupID: Optional[int]
    questionGroupDescription: Optional[str]
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]


class ParticipantModuleGroupAnswer(BaseModel):
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
