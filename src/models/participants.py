from typing import List

from pydantic import BaseModel

from models.questions import Question


class Participant(BaseModel):
    participantID: int
    medicalRecord: str = None
