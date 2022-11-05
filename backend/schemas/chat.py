from typing import List, Optional
from pydantic import BaseModel
from .usuario import Usuario
from .mensagem import  Mensagem
from datetime import date


class ChatBase(BaseModel):
    participantes: List[Usuario]


class ChatUpdate(BaseModel):
    participantes: Optional[List[Usuario]]
    mensagens: Optional[Mensagem]


class ChatCreate(BaseModel):
    id_participantes: List[int]


class Chat(ChatBase):
    id: int
    mensagens: List[Mensagem]

    class Config:
        orm_mode = True


class PaginatedChat(BaseModel):
    limit: int
    offset: int
    data: List[Chat]
