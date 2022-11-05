from typing import Optional, List

from pydantic import BaseModel


class TipoServicoBase(BaseModel):
    nome: str
    cor: str
    icone: str


class TipoServicoUpdate(BaseModel):
    nome: Optional[str]
    cor: Optional[str]
    icone: Optional[str]


class TipoServicoCreate(TipoServicoBase):
    pass


class TipoServico(TipoServicoBase):
    id: int
    class Config:
        orm_mode = True


class PaginatedTipoServico(BaseModel):
    limit: int
    offset: int
    data: List[TipoServico]