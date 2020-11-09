from pydantic import BaseModel
from datetime import datetime

class ModuleRecord(BaseModel):
    formRecordID: int
    crfFormsID: int
    questionnaireID: int
    description: str
    dtRegistroForm: datetime
