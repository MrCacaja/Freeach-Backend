from typing import List, Optional
from pydantic import BaseModel
from .usuario import Usuario
from .habilidade import Habilidade
from .tipo_servico import TipoServico


class ServicoBase(BaseModel):
    titulo: str
    descricao: str
    remoto: bool
    link_imagem: str


class ServicoUpdate(BaseModel):
    status: Optional[int]
    id_contribuinte: Optional[int]
    remoto: Optional[bool]
    id_habilidades: Optional[List[int]]
    id_tipos_servico: Optional[List[int]]
    titulo: Optional[str]
    descricao: Optional[str]
    link_imagem: Optional[str]


class ServicoCreate(ServicoBase):
    id_requisitor: str
    id_habilidades: List[int]
    id_tipos_servico: List[int]


class Servico(ServicoBase):
    id: int
    requisitor: Usuario
    contribuinte: Optional[Usuario]
    habilidades: List[Habilidade]
    tipos_servico: List[TipoServico]

    class Config:
        orm_mode = True


class PaginatedServico(BaseModel):
    limit: int
    offset: int
    data: List[Servico]
