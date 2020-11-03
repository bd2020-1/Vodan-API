import os

import pymysql
import uvicorn as uvicorn
from fastapi import FastAPI

app = FastAPI()

hostname = os.environ.get('MYSQL_HOSTNAME', 'localhost')
database = os.environ.get('MYSQL_DATABASE', 'project_vodan')
username = os.environ.get('MYSQL_USERNAME', 'root')
password = os.environ.get('MYSQL_PASSWORD', '')

db = pymysql.connect(
    host=hostname,
    database=database,
    user=username,
    port=3306,
    password=password,
)
cursor = db.cursor()


async def query_result_to_json(table, query):
    columns_query = f'SHOW COLUMNS FROM {table}'
    cursor.execute(columns_query)
    columns = list(map((lambda v: v[0]), list(cursor.fetchall())))

    cursor.execute(query)
    raw_results = list(cursor.fetchall())
    results = []
    for result in raw_results:
        row = {}
        for idx, column in enumerate(columns):
            row[column] = result[idx]
        results.append(row)
    return results


@app.get("/")
async def read_root():
    return {"API": "Vodan"}


@app.get("/modules")
async def read_modules():
    query = f'SELECT * FROM tb_crfforms'
    response = await query_result_to_json("tb_crfforms", query)
    return {"modules": response}


@app.get("/modules/{module_id}/groups")
async def read_module_groups(module_id: int):
    query = f'SELECT * FROM tb_questiongroupform WHERE crfFormsID={module_id}'
    response = await query_result_to_json("tb_questiongroupform", query)
    return {"groups": response}


@app.get("/groups/{group_id}/questions")
async def read_module_group_questions(group_id: int):
    query = f'SELECT * FROM tb_questions WHERE questionGroupID={group_id}'
    response = await query_result_to_json("tb_questions", query)
    return {"questions": response}


# UNDER CONSTRUCTION
# @app.get("/records/{module_id}")
# async def read_records(module_id: int, group_id: Optional[str] = None, question_id: Optional[str] = None):
#   return { "module_id": module_id, "group_id": group_id, "question_id": question_id }

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=False, workers=3)
