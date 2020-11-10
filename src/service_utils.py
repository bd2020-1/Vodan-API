from config import database
from utils import get_sql_file


async def get_all_modules_from_participant(participant_id: int):
    _query = f"""
        SELECT FM.formRecordID, MO.crfFormsID, MO.questionnaireID, MO.description, FM.dtRegistroForm
        FROM tb_crfforms AS MO LEFT JOIN tb_formrecord AS FM
        ON MO.crfFormsID=FM.crfFormsID
        WHERE participantID = {participant_id}
    """

    modules = await database.fetch_all(_query)

    return modules


async def get_last_filled_module_from_participant(participant_id: int):
    modules = await get_all_modules_from_participant(participant_id)
    module = None
    if modules:
        module = modules[-1]
    return module


async def get_all_modules():
    _query = get_sql_file(file_path_name="select/get_all_modules")

    modules = await database.fetch_all(_query)

    return modules
