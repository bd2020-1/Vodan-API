from pydantic import BaseModel


class Group(BaseModel):
    crfFormsID: int
    questionID: int
    questionOrder: str


