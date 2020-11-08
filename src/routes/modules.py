from typing import List

from fastapi import APIRouter, status

from config import database
from models.questiongroups import QuestionGroups
from models.questions import Question
from models.modules import Module

router = APIRouter()


@router.get("/", response_model=List[Module], status_code=status.HTTP_200_OK)
async def get_all_modules():
    _query = f"""
        SELECT crfFormsID, questionnaireID, description 
        FROM tb_crfforms
    """

    modules = await database.fetch_all(_query)

    return modules

@router.get("/{module_id}", response_model=Module, status_code=status.HTTP_200_OK)
async def get_module(module_id: int):
    _query = f"""
        SELECT crfFormsID, questionnaireID, description 
        FROM tb_crfforms
        WHERE crfFormsID = {module_id}
    """
    module = await database.fetch_all(_query)
    return module

@router.get("/{module_id}/questions", response_model=List[Question], status_code=status.HTTP_200_OK)
async def get_all_questions_from_module(module_id: int):
    _query = f"""
        SELECT crfFormsID, PV.questionID, questionOrder, description, questionTypeID, listTypeID, questionGroupID, subordinateTo, isAbout
        FROM tb_questiongroupform AS PV INNER JOIN tb_questions AS Q
        ON PV.crfFormsID = {module_id} AND PV.questionID = Q.questionID
    """
    questions = await database.fetch_all(_query)

    # Adicionando valores de itens de seleção para perguntas de seleção
    for idx, question in enumerate(questions):
        question = dict(question.items())
        if question['listTypeID']:
            _query = f"""
                SELECT *
                FROM tb_listofvalues
                WHERE listTypeID = {question['listTypeID']}
            """
            values = await database.fetch_all(_query)
            question['ListValues'] = values
        questions[idx] = question
    return questions


@router.get("/{module_id}/questiongroups", response_model=List[QuestionGroups], status_code=status.HTTP_200_OK)
async def get_all_questiongroups_from_module(module_id: int):

    _query = f"""
    SELECT *
    FROM tb_questiongroup
    WHERE questionGroupID IN (
        SELECT questionGroupID
        FROM tb_questiongroupform AS PV INNER JOIN tb_questions AS Q
        ON PV.crfFormsID = {module_id} AND PV.questionID = Q.questionID
        GROUP BY questionGroupID
    )
    """
    questiongroups = await database.fetch_all(_query)

    return questiongroups

