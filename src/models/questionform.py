from pydantic import BaseModel


class QuestionForm(BaseModel):
    crfFormsID: int
    questionID: int
    questionOrder: str


