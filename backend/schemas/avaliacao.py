from typing import Optional, List

from pydantic import BaseModel
from .usuario import Usuario


class AvaliacaoBase(BaseModel):
    comentario: str
    pontuacao: int


class AvaliacaoCreate(AvaliacaoBase):
    id_autor: int
    id_avaliado: int


class AvaliacaoUpdate(AvaliacaoBase):
    comentario: Optional[str]
    pontuacao: Optional[int]


class Avaliacao(AvaliacaoBase):
    id: int
    autor: Usuario
    avaliado: Usuario

    class Config:
        orm_mode = True


class PaginatedAvaliacao(BaseModel):
    limit: int
    offset: int
    data: List[Avaliacao]
