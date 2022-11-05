from typing import List, Optional
from .habilidade import Habilidade
from pydantic import BaseModel


class TipoHabilidadeBase(BaseModel):
    nome: str
    cor: str
    icone: str


class TipoHabilidadeUpdate(BaseModel):
    nome: Optional[str]
    cor: Optional[str]
    icone: Optional[str]


class TipoHabilidadeCreate(TipoHabilidadeBase):
    pass


class TipoHabilidade(TipoHabilidadeBase):
    id: int
    habilidades: List[Habilidade]

    class Config:
        orm_mode = True


class PaginatedTipoHabilidade(BaseModel):
    limit: int
    offset: int
    data: List[TipoHabilidade]
