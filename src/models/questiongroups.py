from pydantic import BaseModel


class QuestionGroups(BaseModel):
    questionGroupID: int
    description: str
    comment: str
