from typing import List, Optional
from .usuario import Usuario
from pydantic import BaseModel


class HabilidadeBase(BaseModel):
    nome: str
    id_tipo_habilidade: int


class HabilidadeCreate(HabilidadeBase):
    pass


class HabilidadeUpdate(BaseModel):
    nome: Optional[str]
    id_tipo_habilidade: Optional[int]
    id_usuarios: Optional[List[int]]


class Habilidade(HabilidadeBase):
    id: int
    usuarios: List[Usuario]

    class Config:
        orm_mode = True


class PaginatedHabilidade(BaseModel):
    limit: int
    offset: int
    data: List[Habilidade]
