from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField

class BookModel(BaseModel):
    id: ObjectIdField = Field(alias="_id")
    title: str
    author: str
    year: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectIdField: str
        }
