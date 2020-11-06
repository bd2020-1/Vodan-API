from typing import List

from fastapi import APIRouter, status

from config import database
from models.questions import Question

router = APIRouter()


@router.get("/{group_id}/questions", response_model=List[Question], status_code=status.HTTP_200_OK)
async def get_all_questions_from_group(group_id: int):
    _query = f"""
        SELECT questionID, description, questionTypeID, listTypeID, questionGroupID, subordinateTo, isAbout
        FROM tb_questions
        WHERE questionGroupID = {group_id}
    """

    questions = await database.fetch_all(_query)

    return questions
