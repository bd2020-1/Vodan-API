from typing import List

from fastapi import APIRouter, status

from config import database
from pydantic import BaseModel
from models.participants import Participant, NewParticipantQuestions
from models.questions import Question
from models.answers import Answer
import sys


from routes.modules import get_all_questions_from_module
from service_utils import get_last_filled_module_from_participant, get_all_modules
from utils import get_sql_file

router = APIRouter()


@router.get("/", response_model=List[Participant], status_code=status.HTTP_200_OK)
async def get_all_participants():
    _query = get_sql_file(file_path_name="select/get_all_participants")

    participants = await database.fetch_all(_query)

    return participants


@router.get(
    "/{participant_id}/nextquestions",
    response_model=List[Question],
    status_code=status.HTTP_200_OK,
)
async def get_next_module_questions_from_participant(participant_id: int):
    last_module = await get_last_filled_module_from_participant(participant_id)
    all_modules = await get_all_modules()

    # Recuperar próximo módulo a ser respondido baseado no ultimo módulo preenchido para esse participante
    if last_module and (all_modules[-1]["crfFormsID"] != last_module["crfFormsID"]):
        next_module = next(
            (m for m in all_modules if [m["crfFormsID"] > last_module["crfFormsID"]])
        )
    else:
        next_module = all_modules[0]

    next_questions = await get_all_questions_from_module(next_module["crfFormsID"])

    return next_questions


# TODO acredito que não deveria ser feito insert nessa rota de GET, poderíamos separar e pra parte da consulta utilizamos
#  a rota /{module_id}/participants/{participant_id}
# FIXME Falta também implementar o id do paciente
@router.get(
    "/newrecord", response_model=NewParticipantQuestions, status_code=status.HTTP_200_OK
)
async def get_participant_questions():
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
    questions = await get_next_module_questions_from_participant(
        participant["participantID"]
    )

    return {"participant": participant, "questions": questions}


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
