from pydantic import BaseModel


class ListValue(BaseModel):
    listOfValuesID: int
    listTypeID: int
    description: str
