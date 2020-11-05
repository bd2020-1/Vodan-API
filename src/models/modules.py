from pydantic import BaseModel


class Module(BaseModel):
    crfFormsID: int
    questionnaireID: int
    description: str
