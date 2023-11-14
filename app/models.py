from typing import List
from pydantic import BaseModel


class ClientModel(BaseModel):
    id: int
    category: str
    firstname: str
    lastname: str
    email: str
    gender: str
    birthdate: str
    
    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.model_fields.keys(), tpl)})


class PageModel(BaseModel):
    total_pages: int
    page_number: int
    data: List[ClientModel]
