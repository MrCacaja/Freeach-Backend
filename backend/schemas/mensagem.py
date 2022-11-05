from typing import List, Optional
from pydantic import BaseModel
from .usuario import Usuario
from datetime import date


class MensagemBase(BaseModel):
    autor: Usuario
    data: date
    conteudo: str


class MensagemUpdate(BaseModel):
    conteudo: Optional[str]


class MensagemCreate(BaseModel):
    id_autor: int
    conteudo: str
    id_chat: int


class Mensagem(MensagemBase):
    id: int
    class Config:
        orm_mode = True


class PaginatedMensagem(BaseModel):
    limit: int
    offset: int
    data: List[Mensagem]
