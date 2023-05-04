from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    item: str
    status: str

class Todo(BaseModel):
    id: int
    item: Item
    class Config:
        schema_extra = {
            "Example": {
                "id": 1,
                "item": {
                    "item": "Example schema!",
                    "status": "new|progress|done"
                    }
                }
            }


class TodoItem(BaseModel):
    item: Item
    class Config:
        schema_extra = {
            "example": {
                "item": {
                    "item": "Read the next chapter of the book",
                    "status": "new|progress|done"
                    }
                }
            }


class TodoItems(BaseModel):
    todos: List[TodoItem]
    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {"item": 
                        {"item": "Example schema 1!", "status": "new|progress|done"}
                    },
                    {"item": 
                        {"item": "Example schema 2!", "status": "new|progress|done"}
                    }
                ]
            }
        }

