from typing import List

from fastapi import APIRouter, status

from config import database
from models.questions import Question
from models.modules import (
    ParticipantModuleAnswer,
    ParticipantModuleGroupAnswer,
    ParticipantModuleDate,
    ParticipantModules,
)
from utils import get_sql_file


router = APIRouter()


@router.get(
    "/{module_id}/questions",
    response_model=List[Question],
    status_code=status.HTTP_200_OK,
)
async def get_all_questions_from_module(module_id: int):
    _query = get_sql_file(file_path_name="select/get_all_questions_from_module").format(
        module_id=module_id
    )
    questions = await database.fetch_all(_query)

    # Adicionando valores de itens de seleção para perguntas de seleção
    for idx, question in enumerate(questions):
        question = dict(question.items())
        if question["listTypeID"]:
            _query = f"""
                SELECT *
                FROM tb_listofvalues
                WHERE listTypeID = {question['listTypeID']}
            """
            values = await database.fetch_all(_query)
            question["ListValues"] = values
        questions[idx] = question
    return questions


@router.get(
    "/{module_id}/participants/{participant_id}",
    response_model=List[ParticipantModuleAnswer],
    status_code=status.HTTP_200_OK,
)
async def get_all_answers_from_module_per_participant(
    module_id: int, participant_id: int
):
    _query = get_sql_file(
        file_path_name="select/get_answers_per_participant_per_module"
    ).format(module_id=module_id, participant_id=participant_id)

    groups = await database.fetch_all(_query)

    return groups


@router.get(
    "/{module_id}/questions/{participant_id}",
    response_model=List[ParticipantModuleDate],
    status_code=status.HTTP_200_OK,
)
async def get_all_answers_from_module_per_participant_per_date(
    module_id: int, participant_id: int, data_attendance: str = None
):
    _query = get_sql_file(
        file_path_name="select/get_answers_per_participant_per_date"
    ).format(
        module_id=module_id,
        participant_id=participant_id,
        data_attendance=data_attendance,
    )

    groups = await database.fetch_all(_query)

    return groups


@router.get(
    "/participants/{participant_id}/modules",
    response_model=List[ParticipantModules],
    status_code=status.HTTP_200_OK,
)
async def get_all_modules_from_participant(participant_id: int):
    _query = get_sql_file(
        file_path_name="select/get_all_modules_per_participant"
    ).format(participant_id=participant_id)

    groups = await database.fetch_all(_query)

    return groups


@router.get(
    "/{module_id}/groups/{group_id}/participants/{participant_id}",
    response_model=List[ParticipantModuleGroupAnswer],
    status_code=status.HTTP_200_OK,
)
async def get_all_answers_from_module_group_per_participant(
    module_id: int, group_id: int, participant_id: int
):
    _query = get_sql_file(
        file_path_name="select/get_answers_per_participant_per_module_group"
    ).format(module_id=module_id, group_id=group_id, participant_id=participant_id)

    groups = await database.fetch_all(_query)

    return groups
