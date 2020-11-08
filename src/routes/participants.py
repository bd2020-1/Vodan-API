from typing import List, Dict

from fastapi import APIRouter, status

from config import database
from models.modulesrecords import ModuleRecord
from models.modules import Module
from models.participants import Participant, NewParticipantQuestions
from models.questions import Question

from routes.modules import get_all_modules, get_all_questions_from_module

router = APIRouter()


@router.get("/", response_model=List[Participant], status_code=status.HTTP_200_OK)
async def get_all_participants():
    _query = f"""
        SELECT participantID, medicalRecord 
        FROM tb_participant
    """

    participants = await database.fetch_all(_query)

    return participants



@router.get("/{participant_id}/records", response_model=List[ModuleRecord], status_code=status.HTTP_200_OK, )
async def get_all_modules_from_participant(participant_id: int):
    _query = f"""
        SELECT FM.formRecordID, MO.crfFormsID, MO.questionnaireID, MO.description, FM.dtRegistroForm
        FROM tb_crfforms AS MO LEFT JOIN tb_formrecord AS FM
        ON MO.crfFormsID=FM.crfFormsID
        WHERE participantID = {participant_id}
    """

    modules = await database.fetch_all(_query)

    return modules

# @router.get("/{participant_id}/lastrecord", response_model=ModuleRecord, status_code=status.HTTP_200_OK)
async def get_last_filled_module_from_participant(participant_id: int):
    modules = await get_all_modules_from_participant(participant_id)
    module = None
    if modules: module = modules[-1]
    return module


@router.get("/{participant_id}/nextquestions", response_model=List[Question], status_code=status.HTTP_200_OK)
async def get_next_module_questions_from_participant(participant_id: int):
    last_module = await get_last_filled_module_from_participant(participant_id)
    all_modules = await get_all_modules()
    
    # Recuperar próximo módulo a ser respondido baseado no ultimo módulo preenchido para esse participante
    if last_module and ( all_modules[-1]['crfFormsID'] != last_module['crfFormsID']):
        next_module = next((m for m in all_modules if [m['crfFormsID'] > last_module['crfFormsID']]))
    else:
        next_module = all_modules[0]

    next_questions = await get_all_questions_from_module(next_module['crfFormsID'])

    return next_questions



@router.get("/newrecord", response_model=NewParticipantQuestions, status_code=status.HTTP_200_OK)
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
    questions = await get_next_module_questions_from_participant(participant['participantID'])

    return {
        "participant": participant,
        "questions": questions
    } 