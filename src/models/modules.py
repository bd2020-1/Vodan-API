from typing import Optional
from pydantic.main import BaseModel
from datetime import date


class ParticipantModuleAnswer(BaseModel):
    questionGroupID: Optional[int]
    questionGroupDescription: Optional[str]
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
    listParticipantAnswer: Optional[str]


class ParticipantModuleAnswerWithFormID(BaseModel):
    crfFormsID: int
    questionGroupID: Optional[int]
    questionGroupDescription: Optional[str]
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
    listParticipantAnswer: Optional[str]


class ParticipantModuleGroupAnswer(BaseModel):
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
    listParticipantAnswer: Optional[str]


class FormModule(BaseModel):
    crfFormsID: int
    description: str


class ParticipantModules(BaseModel):
    formRecordID: int
    dtRegisterForm: Optional[date]
    crfFormsID: int
    FormsName: str

class ParticipantModuleDate(BaseModel):
    questionID: int
    questionDescription: str
    participantAnswer: Optional[str]
    listParticipantAnswer: Optional[str]


class QuestionGroups(BaseModel):
    questionGroupID: int
    description: str
    comment: str
