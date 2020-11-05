from typing import List

from fastapi import APIRouter, status

from config import database
from models.groups import Group
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


@router.get("/{module_id}/groups", response_model=List[Group], status_code=status.HTTP_200_OK)
async def get_all_groups_from_module(module_id: int):
    _query = f"""
        SELECT crfFormsID, questionID, questionOrder 
        FROM tb_questiongroupform 
        WHERE crfFormsID = {module_id}
    """

    groups = await database.fetch_all(_query)

    return groups
