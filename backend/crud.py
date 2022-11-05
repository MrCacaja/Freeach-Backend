import copy
import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

import models
from schemas import usuario, tipo_habilidade, tipo_servico, servico, mensagem, avaliacao, habilidade, chat
from exceptions import UsuarioAlreadyExistError, UsuarioNotFoundError, TipoHabilidadeNotFoundError, \
    TipoServicoNotFoundError, ServicoNotFoundError, MensagemNotFoundError, AvaliacaoNotFoundError, \
    HabilidadeNotFoundError, ChatNotFound


# usuário

def check_usuario(db: Session, usuario: usuario.UsuarioLoginSchema):
    db_usuario = db.query(models.Usuario).filter(
        and_(models.Usuario.email == usuario.email, models.Usuario.senha == usuario.senha)).first()
    return db_usuario is not None


def get_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).get(usuario_id)
    if db_usuario is None:
        raise UsuarioNotFoundError
    return db_usuario


def get_all_usuarios(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).offset(offset).limit(limit).all()


def get_usuario_by_email(db: Session, usuario_email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == usuario_email).first()


def create_usuario(db: Session, usuario: usuario.UsuarioCreate):
    db_usuario = get_usuario_by_email(db, usuario.email)
    if db_usuario is not None:
        raise UsuarioAlreadyExistError
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, usuario_id: int, usuario: usuario.UsuarioUpdate):
    db_usuario = get_usuario_by_id(db, usuario_id)
    for property in usuario:
        if property[1] is not None:
            setattr(db_usuario, property[0], property[1])
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def delete_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db.delete(db_usuario)
    db.commit()


# tipo habilidade


def create_tipo_habilidade(db: Session, tipo_habilidade: tipo_habilidade.TipoHabilidadeCreate):
    db_tipo_habilidade = models.TipoHabilidade(**tipo_habilidade.dict())
    db.add(db_tipo_habilidade)
    db.commit()
    db.refresh(db_tipo_habilidade)
    return db_tipo_habilidade


def get_all_tipos_habilidade(db: Session, offset: int, limit: int):
    return db.query(models.TipoHabilidade).offset(offset).limit(limit).all()


def get_tipo_habilidade_by_id(db: Session, tipo_habilidade_id: int):
    db_tipo_habilidade = db.query(models.TipoHabilidade).get(tipo_habilidade_id)
    if db_tipo_habilidade is None:
        raise TipoHabilidadeNotFoundError
    return db_tipo_habilidade


def update_tipo_habilidade(db: Session, tipo_habilidade_id: int, tipo_habilidade: tipo_habilidade.TipoHabilidadeUpdate):
    db_tipo_habilidade = get_tipo_habilidade_by_id(db, tipo_habilidade_id)
    for property in tipo_habilidade:
        if property[1] is not None:
            setattr(db_tipo_habilidade, property[0], property[1])
    db.commit()
    db.refresh(db_tipo_habilidade)
    return db_tipo_habilidade


def delete_tipo_habilidade_by_id(db: Session, tipo_habilidade_id: int):
    db_tipo_habilidade = get_tipo_habilidade_by_id(db, tipo_habilidade_id)
    db.delete(db_tipo_habilidade)
    db.commit()


# habilidade


def create_habilidade(db: Session, habilidade: habilidade.HabilidadeCreate):
    db_habilidade = models.Habilidade(**habilidade.dict())
    if get_tipo_habilidade_by_id(db, db_habilidade.id_tipo_habilidade) is None:
        raise TipoHabilidadeNotFoundError
    db.add(db_habilidade)
    db.commit()
    db.refresh(db_habilidade)
    return db_habilidade


def get_all_habilidades(db: Session, offset: int, limit: int):
    return db.query(models.Habilidade).options().offset(offset).limit(limit).all()


def get_habilidade_by_id(db: Session, habilidade_id: int):
    db_habilidade = db.query(models.Habilidade).get(habilidade_id)
    if db_habilidade is None:
        raise HabilidadeNotFoundError
    return db_habilidade


def update_habilidade(db: Session, habilidade_id: int, habilidade: habilidade.HabilidadeUpdate):
    db_habilidade = get_habilidade_by_id(db, habilidade_id)
    for property in habilidade:
        if property[1] is not None:
            setattr(db_habilidade, property[0], property[1])
    if habilidade.id_usuarios is not None:
        db_habilidade.usuarios = []
        for id_usuario in habilidade.id_usuarios:
            db_habilidade.usuarios.append(get_usuario_by_id(db, id_usuario))
    db.commit()
    db.refresh(db_habilidade)
    return db_habilidade


def delete_habilidade_by_id(db: Session, habilidade_id: int):
    db_habilidade = get_habilidade_by_id(db, habilidade_id)
    db.delete(db_habilidade)
    db.commit()


# tipo servico


def create_tipo_servico(db: Session, tipo_servico: tipo_servico.TipoServicoCreate):
    db_tipo_servico = models.TipoServico(**tipo_servico.dict())
    db.add(db_tipo_servico)
    db.commit()
    db.refresh(db_tipo_servico)
    return db_tipo_servico


def get_all_tipos_servico(db: Session, offset: int, limit: int):
    return db.query(models.TipoServico).offset(offset).limit(limit).all()


def get_tipo_servico_by_id(db: Session, tipo_servico_id: int):
    db_tipo_servico = db.query(models.TipoServico).get(tipo_servico_id)
    if db_tipo_servico is None:
        raise TipoServicoNotFoundError
    return db_tipo_servico


def update_tipo_servico(db: Session, tipo_servico_id: int, tipo_servico: tipo_servico.TipoServicoUpdate):
    db_tipo_servico = get_tipo_servico_by_id(db, tipo_servico_id)
    for property in tipo_servico:
        if property[1] is not None:
            setattr(db_tipo_servico, property[0], property[1])
    db.commit()
    db.refresh(db_tipo_servico)
    return db_tipo_servico


def delete_tipo_servico_by_id(db: Session, tipo_servico_id: int):
    db_tipo_servico = get_tipo_servico_by_id(db, tipo_servico_id)
    db.delete(db_tipo_servico)
    db.commit()


# servico


def create_servico(db: Session, servico: servico.ServicoCreate):
    id_habilidades = copy.copy(servico.id_habilidades)
    id_tipos_servico = copy.copy(servico.id_tipos_servico)
    del servico.id_habilidades
    del servico.id_tipos_servico
    db_servico = models.Servico(**servico.dict())
    db_servico.habilidades = []
    for id_habilidade in id_habilidades:
        db_servico.habilidades.append(get_habilidade_by_id(db, id_habilidade))
    for id_tipo_servico in id_tipos_servico:
        db_servico.tipos_servico.append(get_tipo_servico_by_id(db, id_tipo_servico))
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico


def get_all_servicos(db: Session, offset: int, limit: int):
    return db.query(models.Servico).offset(offset).limit(limit).all()


def get_servico_by_id(db: Session, servico_id: int):
    db_servico = db.query(models.Servico).get(servico_id)
    if db_servico is None:
        raise ServicoNotFoundError
    return db_servico


def update_servico(db: Session, servico_id: int, servico: servico.ServicoUpdate):
    db_servico = get_servico_by_id(db, servico_id)
    if servico.id_habilidades is not None:
        db_servico.habilidades = []
        for id_habilidade in servico.id_habilidades:
            db_servico.habilidades.append(get_usuario_by_id(db, id_habilidade))
    if servico.id_tipos_servico is not None:
        db_servico.tipos_servico = []
        for id_tipo_servico in servico.id_tipos_servico:
            db_servico.tipos_servico.append(get_usuario_by_id(db, id_tipo_servico))
    for property in servico:
        if property[1] is not None:
            setattr(db_servico, property[0], property[1])
    db.commit()
    db.refresh(db_servico)
    return db_servico


def delete_servico_by_id(db: Session, servico_id: int):
    db_servico = get_servico_by_id(db, servico_id)
    db.delete(db_servico)
    db.commit()


# mensagem


def create_mensagem(db: Session, mensagem: mensagem.MensagemCreate):
    chat = get_chat_by_id(db, mensagem.id_chat)
    del mensagem.id_chat
    db_mensagem = models.Mensagem(**mensagem.dict())
    db_mensagem.chat = [chat]
    db_mensagem.data = datetime.datetime.now()
    db.add(db_mensagem)
    db.commit()
    db.refresh(db_mensagem)
    return db_mensagem


def get_all_mensagens(db: Session, offset: int, limit: int):
    return db.query(models.Mensagem).offset(offset).limit(limit).all()


def get_mensagem_by_id(db: Session, mensagem_id: int):
    db_mensagem = db.query(models.Mensagem).get(mensagem_id)
    if db_mensagem is None:
        raise MensagemNotFoundError
    return db_mensagem


def update_mensagem(db: Session, mensagem_id: int, mensagem: mensagem.MensagemUpdate):
    db_mensagem = get_mensagem_by_id(db, mensagem_id)
    for property in mensagem:
        if property[1] is not None:
            setattr(db_mensagem, property[0], property[1])
    db.commit()
    db.refresh(db_mensagem)
    return db_mensagem


def delete_mensagem_by_id(db: Session, mensagem_id: int):
    db_mensagem = get_mensagem_by_id(db, mensagem_id)
    db.delete(db_mensagem)
    db.commit()


# avaliacao


def create_avaliacao(db: Session, avaliacao: avaliacao.AvaliacaoCreate):
    get_usuario_by_id(db, avaliacao.id_autor)
    get_usuario_by_id(db, avaliacao.id_avaliado)
    db_avaliacao = models.Avaliacao(**avaliacao.dict())
    db.add(db_avaliacao)
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao


def get_all_avaliacoes(db: Session, offset: int, limit: int):
    return db.query(models.Avaliacao).offset(offset).limit(limit).all()


def get_avaliacao_by_id(db: Session, avaliacao_id: int):
    db_avaliacao = db.query(models.Avaliacao).get(avaliacao_id)
    if db_avaliacao is None:
        raise AvaliacaoNotFoundError
    return db_avaliacao


def update_avaliacao(db: Session, avaliacao_id: int, avaliacao: avaliacao.AvaliacaoUpdate):
    db_avaliacao = get_avaliacao_by_id(db, avaliacao_id)
    for property in avaliacao:
        if property[1] is not None:
            setattr(db_avaliacao, property[0], property[1])
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao


def delete_avaliacao_by_id(db: Session, avaliacao_id: int):
    db_avaliacao = get_avaliacao_by_id(db, avaliacao_id)
    db.delete(db_avaliacao)
    db.commit()


# chat


def create_chat(db: Session, chat: chat.ChatCreate):
    participantes = []
    for id_participante in chat.id_participantes:
        participantes.append(get_usuario_by_id(db, id_participante))
    del chat.id_participantes
    db_chat = models.Chat(**chat.dict())
    db_chat.participantes = participantes
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_all_chats(db: Session, offset: int, limit: int):
    return db.query(models.Chat).offset(offset).limit(limit).all()


def get_chat_by_id(db: Session, chat_id: int):
    db_chat = db.query(models.Chat).get(chat_id)
    if db_chat is None:
        raise ChatNotFound
    return db_chat


def update_chat(db: Session, chat_id: int, chat: chat.ChatUpdate):
    db_chat = get_chat_by_id(db, chat_id)
    for property in chat:
        if property[1] is not None:
            setattr(db_chat, property[0], property[1])
    db.commit()
    db.refresh(db_chat)
    return db_chat


def delete_chat_by_id(db: Session, chat_id: int):
    db_chat = get_chat_by_id(db, chat_id)
    db.delete(db_chat)
    db.commit()
