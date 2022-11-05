from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session

import crud
import models
import schemas
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from database import get_db, engine
from exceptions import UsuarioException, TipoHabilidadeException, TipoServicoException, ServicoException, \
    MensagemException, AvaliacaoException, HabilidadeException, ChatException

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# usuário

@app.get("/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.usuario.Usuario)
def get_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)


@app.get("/usuarios", dependencies=[Depends(JWTBearer())], response_model=schemas.usuario.PaginatedUsuario)
def get_all_usuarios(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_usuarios = crud.get_all_usuarios(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_usuarios}
    return response


@app.post("/usuarios", dependencies=[Depends(JWTBearer())], response_model=schemas.usuario.Usuario)
def create_usuario(usuario: schemas.usuario.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.usuario.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.usuario.UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_usuario(db, usuario_id, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())])
def delete_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)


# login
@app.post("/signup", tags=["usuario"])
async def create_usuario_signup(usuario: schemas.usuario.UsuarioCreate = Body(...), db: Session = Depends(get_db)):
    try:
        crud.create_usuario(db, usuario)
        return signJWT(usuario.email)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/login", tags=["usuario"])
async def user_login(usuario: schemas.usuario.UsuarioLoginSchema = Body(...), db: Session = Depends(get_db)):
    if crud.check_usuario(db, usuario):
        return signJWT(usuario.email)
    return {
        "error": "E-mail ou senha incorretos!"
    }

# tipo de habilidade

@app.get("/tipo_habilidade", dependencies=[Depends(JWTBearer())], response_model=schemas.tipo_habilidade.PaginatedTipoHabilidade)
def get_all_tipos_habilidade(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_tipos_habilidade = crud.get_all_tipos_habilidade(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_tipos_habilidade}
    return response


@app.get("/tipo_habilidade/{tipo_habilidade_id}", dependencies=[Depends(JWTBearer)], response_model=schemas.tipo_habilidade.TipoHabilidade)
def get_tipo_habilidade_by_id(tipo_habilidade_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_tipo_habilidade_by_id(db, tipo_habilidade_id)
    except TipoHabilidadeException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/tipo_habilidade", tags=["tipo_habilidade"])
async def create_tipo_habilidade(tipo_habilidade: schemas.tipo_habilidade.TipoHabilidadeCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.create_tipo_habilidade(db, tipo_habilidade)
    except TipoHabilidadeException as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/tipo_habilidade/{tipo_habilidade_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.tipo_habilidade.TipoHabilidade)
def update_tipo_habilidade(tipo_habilidade_id: int, tipo_habilidade: schemas.tipo_habilidade.TipoHabilidadeUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_tipo_habilidade(db, tipo_habilidade_id, tipo_habilidade)
    except TipoHabilidadeException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/tipo_habilidade/{tipo_habilidade_id}", dependencies=[Depends(JWTBearer())])
def delete_tipo_habilidade_by_id(tipo_habilidade_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_tipo_habilidade_by_id(db, tipo_habilidade_id)
    except TipoHabilidadeException as cie:
        raise HTTPException(**cie.__dict__)


# habilidade

@app.get("/habilidade", dependencies=[Depends(JWTBearer())], response_model=schemas.habilidade.PaginatedHabilidade)
def get_all_habilidades(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_habilidade = crud.get_all_habilidades(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_habilidade}
    return response


@app.get("/habilidade/{habilidade_id}", dependencies=[Depends(JWTBearer)], response_model=schemas.habilidade.Habilidade)
def get_habilidade_by_id(habilidade_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_habilidade_by_id(db, habilidade_id)
    except HabilidadeException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/habilidade", tags=["habilidade"])
async def create_habilidade(habilidade: schemas.habilidade.HabilidadeCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.create_habilidade(db, habilidade)
    except (HabilidadeException, TipoHabilidadeException) as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/habilidade/{habilidade_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.habilidade.Habilidade)
def update_habilidade(habilidade_id: int, habilidade: schemas.habilidade.HabilidadeUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_habilidade(db, habilidade_id, habilidade)
    except HabilidadeException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/habilidade/{habilidade_id}", dependencies=[Depends(JWTBearer())])
def delete_habilidade_by_id(habilidade_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_habilidade_by_id(db, habilidade_id)
    except HabilidadeException as cie:
        raise HTTPException(**cie.__dict__)


# tipo de servico

@app.get("/tipo_servico", dependencies=[Depends(JWTBearer())], response_model=schemas.tipo_servico.PaginatedTipoServico)
def get_all_tipos_servico(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_tipos_servico = crud.get_all_tipos_servico(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_tipos_servico}
    return response


@app.get("/tipo_servico/{tipo_servico_id}", dependencies=[Depends(JWTBearer)], response_model=schemas.tipo_servico.TipoServico)
def get_tipo_servico_by_id(tipo_servico_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_tipo_servico_by_id(db, tipo_servico_id)
    except TipoServicoException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/tipo_servico", tags=["tipo_servico"])
async def create_tipo_servico(tipo_servico: schemas.tipo_servico.TipoServicoCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.create_tipo_servico(db, tipo_servico)
    except TipoServicoException as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/tipo_servico/{tipo_servico_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.tipo_servico.TipoServico)
def update_tipo_servico(tipo_servico_id: int, tipo_servico: schemas.tipo_servico.TipoServicoUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_tipo_servico(db, tipo_servico_id, tipo_servico)
    except TipoServicoException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/tipo_servico/{tipo_servico_id}", dependencies=[Depends(JWTBearer())])
def delete_tipo_servico_by_id(tipo_servico_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_tipo_servico_by_id(db, tipo_servico_id)
    except TipoServicoException as cie:
        raise HTTPException(**cie.__dict__)


# servico

@app.get("/servico", dependencies=[Depends(JWTBearer())], response_model=schemas.servico.PaginatedServico)
def get_all_servicos(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_servicos = crud.get_all_servicos(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_servicos}
    return response


@app.get("/servico/{servico_id}", dependencies=[Depends(JWTBearer)], response_model=schemas.servico.Servico)
def get_servico_by_id(servico_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_servico_by_id(db, servico_id)
    except ServicoException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/servico", tags=["servico"])
async def create_servico(servico: schemas.servico.ServicoCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.create_servico(db, servico)
    except ServicoException as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/servico/{servico_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.servico.Servico)
def update_servico(servico_id: int, servico: schemas.servico.ServicoUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_servico(db, servico_id, servico)
    except ServicoException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/servico/{servico_id}", dependencies=[Depends(JWTBearer())])
def delete_servico_by_id(servico_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_servico_by_id(db, servico_id)
    except ServicoException as cie:
        raise HTTPException(**cie.__dict__)


# mensagem

@app.get("/mensagem", dependencies=[Depends(JWTBearer())], response_model=schemas.mensagem.PaginatedMensagem)
def get_all_mensagens(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_mensagens = crud.get_all_mensagens(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_mensagens}
    return response


@app.get("/mensagem/{mensagem_id}", dependencies=[Depends(JWTBearer)], response_model=schemas.mensagem.Mensagem)
def get_mensagem_by_id(mensagem_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_mensagem_by_id(db, mensagem_id)
    except MensagemException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/mensagem", tags=["mensagem"])
async def create_mensagem(mensagem: schemas.mensagem.MensagemCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.create_mensagem(db, mensagem)
    except MensagemException as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/mensagem/{mensagem_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.mensagem.Mensagem)
def update_mensagem(mensagem_id: int, mensagem: schemas.mensagem.MensagemUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_mensagem(db, mensagem_id, mensagem)
    except MensagemException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/mensagem/{mensagem_id}", dependencies=[Depends(JWTBearer())])
def delete_mensagem_by_id(mensagem_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_mensagem_by_id(db, mensagem_id)
    except MensagemException as cie:
        raise HTTPException(**cie.__dict__)


# avaliação


@app.get("/avaliacao", dependencies=[Depends(JWTBearer())], response_model=schemas.avaliacao.PaginatedAvaliacao)
def get_all_avaliacoes(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_avaliacoes = crud.get_all_avaliacoes(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_avaliacoes}
    return response


@app.get("/avaliacao/{avaliacao_id}", dependencies=[Depends(JWTBearer)], response_model=schemas.avaliacao.Avaliacao)
def get_avaliacao_by_id(avaliacao_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_avaliacao_by_id(db, avaliacao_id)
    except AvaliacaoException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/avaliacao", tags=["avaliacao"])
async def create_avaliacao(avaliacao: schemas.avaliacao.AvaliacaoCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.create_avaliacao(db, avaliacao)
    except (AvaliacaoException, UsuarioException) as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/avaliacao/{avaliacao_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.avaliacao.Avaliacao)
def update_avaliacao(avaliacao_id: int, avaliacao: schemas.avaliacao.AvaliacaoUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_avaliacao(db, avaliacao_id, avaliacao)
    except AvaliacaoException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/avaliacao/{avaliacao_id}", dependencies=[Depends(JWTBearer())])
def delete_avaliacao_by_id(avaliacao_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_avaliacao_by_id(db, avaliacao_id)
    except AvaliacaoException as cie:
        raise HTTPException(**cie.__dict__)


# chat


@app.get("/chat", dependencies=[Depends(JWTBearer())], response_model=schemas.chat.PaginatedChat)
def get_all_chats(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_chats = crud.get_all_chats(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_chats}
    return response


@app.get("/chat/{chat_id}", dependencies=[Depends(JWTBearer)], response_model=schemas.chat.Chat)
def get_chat_by_id(chat_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_chat_by_id(db, chat_id)
    except ChatException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/chat", tags=["chat"])
async def create_chat(chat: schemas.chat.ChatCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.create_chat(db, chat)
    except (ChatException, UsuarioException) as cie:
        raise HTTPException(**cie.__dict__)


@app.put("/chat/{chat_id}", dependencies=[Depends(JWTBearer())], response_model=schemas.chat.ChatUpdate)
def update_chat(chat_id: int, chat: schemas.chat.ChatUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_chat(db, chat_id, chat)
    except ChatException as cie:
        raise HTTPException(**cie.__dict__)


@app.delete("/chat/{chat_id}", dependencies=[Depends(JWTBearer())])
def delete_chat_by_id(chat_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_chat_by_id(db, chat_id)
    except ChatException as cie:
        raise HTTPException(**cie.__dict__)
