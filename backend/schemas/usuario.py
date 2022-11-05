from typing import List, Optional
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str
    email: str


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str]
    senha: Optional[str]


class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True


class UsuarioLoginSchema(BaseModel):
    email: str
    senha: str


class PaginatedUsuario(BaseModel):
    limit: int
    offset: int
    data: List[Usuario]


Usuario.update_forward_refs()
