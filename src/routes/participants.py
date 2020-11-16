from typing import List

from fastapi import APIRouter, status

from config import database
from pydantic import BaseModel

from models.modules import FormModule, ParticipantModuleAnswerWithFormID
from models.participants import Participant
from models.modules import (
    ParticipantModules,
)
from models.modules import (
    ParticipantModuleAnswer,
    ParticipantModuleGroupAnswer,
    ParticipantModuleDate,
)
from models.answers import Answer
import sys

from utils import get_sql_file


router = APIRouter()


@router.get("/", response_model=List[Participant], status_code=status.HTTP_200_OK)
async def get_all_participants():
    _query = get_sql_file(file_path_name="select/get_all_participants")

    participants = await database.fetch_all(_query)

    return participants


@router.get(
    "/{participant_id}/modules/available",
    response_model=List[FormModule],
    status_code=status.HTTP_200_OK,
)
async def get_next_modules_available_from_participant(participant_id: int):
    _query_last_module_filled = get_sql_file(
        file_path_name="select/get_last_module_filled_by_participant"
    ).format(participant_id=participant_id)
    last_module_filled = await database.fetch_one(_query_last_module_filled)

    if last_module_filled:
        if last_module_filled["crfFormsID"] == 3:
            _query = """SELECT crfFormsID, description FROM project_vodan.tb_crfforms WHERE description LIKE '%Admission%'"""
            next_modules_available = await database.fetch_all(_query)
        else:
            _query = """SELECT crfFormsID, description FROM project_vodan.tb_crfforms WHERE description NOT LIKE '%Admission%'"""
            next_modules_available = await database.fetch_all(_query)
    else:
        _query = """SELECT crfFormsID, description FROM project_vodan.tb_crfforms WHERE description LIKE '%Admission%'"""
        next_modules_available = await database.fetch_all(_query)

    return next_modules_available


@router.post("/", response_model=Participant, status_code=status.HTTP_200_OK)
async def new_participant():
    _query = f"""
        START TRANSACTION;
        SELECT @last_id:=max(participantID)+1 
        FROM tb_participant;
        INSERT INTO tb_participant ( participantID )
        VALUES  (@last_id);
        COMMIT;
    """
    await database.execute(_query)
    _query = f"""
        SELECT *
        FROM tb_participant
        ORDER BY participantID DESC
    """
    participant = await database.fetch_one(_query)

    return participant


class AnsBody(BaseModel):
    answers: List[Answer]


@router.post("/{participant_id}/newrecord/{module_id}", status_code=status.HTTP_200_OK)
async def post_participant_answers(participant_id: int, module_id: int, body: AnsBody):
    try:
        await database.execute(
            """
            SET autocommit=0;
            START TRANSACTION
        """
        )
        answers = dict(body)["answers"]
        # Cria um assessmentquestionnaire para o participante caso não exista
        # OBS: hospitalUnitID e questionnaireID são constantes por enquanto
        _query = f"""
            INSERT INTO tb_assessmentquestionnaire (participantID, hospitalUnitID, questionnaireID)
            SELECT * FROM (SELECT {participant_id} as participantID, 1 as hospitalUnitID, 1 as questionnaireID) AS tmp
            WHERE NOT EXISTS (
                SELECT participantID FROM tb_assessmentquestionnaire WHERE participantID = {participant_id}
            ) LIMIT 1;
        """
        await database.execute(_query)

        # Descobre o maior formRecordID preenchido pela ultima resposta
        _query = f"""
            SELECT *
            FROM tb_formrecord
            ORDER BY formRecordID DESC
        """
        next_form_record_id = (await database.fetch_one(_query))["formRecordID"] + 1

        # Cria o formRecord
        _query = f"""
            INSERT INTO tb_formrecord (formRecordID, participantID, hospitalUnitID, questionnaireID, crfFormsID)
            VALUES ({next_form_record_id}, {participant_id}, 1, 1, {module_id})
        """
        await database.execute(_query)
        _query = f"""
            SELECT *
            FROM tb_formrecord
            ORDER BY questionGroupFormRecordID DESC
        """

        # Descobre o maior questiongroupformrecordID preenchido pela ultima resposta
        _query = f"""
            SELECT *
            FROM tb_questiongroupformrecord
            ORDER BY questionGroupFormRecordID DESC
        """
        next_ans_id = (await database.fetch_one(_query))[
            "questionGroupFormRecordID"
        ] + 1

        # Cria a resposta para cada resposta enviada
        _query = f"""   
            INSERT INTO tb_questiongroupformrecord (questionGroupFormRecordID, formRecordId, crfFormsID, questionID, listOfValuesID, answer)
            VALUES (:questionGroupFormRecordID, :formRecordId, :crfFormsID, :questionID, :listOfValuesID, :answer)
        """
        _values = []
        for ans in answers:
            value = dict(ans)
            value.update(
                {
                    "questionGroupFormRecordID": next_ans_id,
                    "formRecordId": next_form_record_id,
                    "crfFormsID": module_id,
                }
            )
            _values.append(value)
            next_ans_id += 1
        await database.execute_many(query=_query, values=_values)
    except:
        await database.execute(
            """
            ROLLBACK;
            SET autocommit=1
        """
        )
        return {
            "erro": f"Erro ao registrar respostas:  {sys.exc_info()[0]}",
        }
    else:
        await database.execute(
            """
            COMMIT;
            SET autocommit=1
        """
        )
        return {
            "sucesso": "Respostas registradas com sucesso",
        }


@router.get(
    "/{participant_id}/modules/{module_id}",
    response_model=List[ParticipantModuleAnswer],
    status_code=status.HTTP_200_OK,
)
async def get_all_answers_from_module_per_participant(
    participant_id: int, module_id: int
):
    _query = get_sql_file(
        file_path_name="select/get_answers_per_participant_per_module"
    ).format(module_id=module_id, participant_id=participant_id)

    groups = await database.fetch_all(_query)

    return groups


@router.get(
    "/{participant_id}/last/module",
    response_model=List[ParticipantModuleAnswerWithFormID],
    status_code=status.HTTP_200_OK,
)
async def get_last_module_answer(participant_id: int):
    _query = get_sql_file(
        file_path_name="select/get_last_answers_per_participant_per_module"
    ).format(participant_id=participant_id)

    groups = await database.fetch_all(_query)

    return groups


@router.get(
    "/{participant_id}/questions/{module_id}",
    response_model=List[ParticipantModuleDate],
    status_code=status.HTTP_200_OK,
)
async def get_all_answers_from_module_per_participant_per_date(
    participant_id: int, module_id: int, data_attendance: str = None
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
    "/{participant_id}/modules",
    response_model=List[ParticipantModules],
    status_code=status.HTTP_200_OK,
)
async def get_all_modules_from_participant(
    participant_id: int, list_modules: str = None
):

    if not list_modules:
        list_modules = [1, 2, 3]
    else:
        list_modules = list(list_modules.split(","))

    _query = get_sql_file(
        file_path_name="select/get_all_modules_per_participant"
    ).format(participant_id=participant_id, tuple_modules=tuple(list_modules))

    groups = await database.fetch_all(_query)

    return groups


@router.get(
    "/{participant_id}/modules/{module_id}/groups",
    response_model=List[ParticipantModuleGroupAnswer],
    status_code=status.HTTP_200_OK,
)
async def get_all_answers_from_module_group_per_participant(
    participant_id: int, module_id: int, list_groups: str = None
):
    if not list_groups:
        list_groups = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    else:
        list_groups = list(list_groups.split(","))

    _query = get_sql_file(
        file_path_name="select/get_answers_per_participant_per_module_group"
    ).format(
        module_id=module_id,
        participant_id=participant_id,
        list_groups=tuple(list_groups),
    )

    groups = await database.fetch_all(_query)

    return groups
