from typing import Optional
from pydantic.main import BaseModel
from datetime import datetime, time, timedelta


class ParticipantModuleAnswer(BaseModel):
    questionGroupID: Optional[int]
    questionGroupDescription: Optional[str]
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
    listOfValuesID: Optional[int]
    listParticipantAnswer: Optional[str]


class ParticipantModuleGroupAnswer(BaseModel):
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
    listOfValuesID: Optional[int]
    listParticipantAnswer: Optional[str]


class FormModule(BaseModel):
    crfFormsID: int
    description: str


class ParticipantModules(BaseModel):
    formRecordID: int
    dtRegistroForm: Optional[datetime]
    crfFormsID: int
    
    
class ParticipantModuleDate(BaseModel):
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
    description: Optional[str]
