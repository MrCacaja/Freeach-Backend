from sqlalchemy import DateTime, SmallInteger, Column, ForeignKey, Integer, String, Boolean, ARRAY, Table
from sqlalchemy.orm import relationship
from database import Base

RelacaoUsuarioHabilidade = Table(
    "relacao_usuario_habilidade",
    Base.metadata,
    Column("id_habilidade", ForeignKey("habilidades.id"), primary_key=True),
    Column("id_usuario", ForeignKey("usuarios.id"), primary_key=True),
)


RelacaoServicoHabilidade = Table(
    "relacao_servico_habilidade",
    Base.metadata,
    Column("id_habilidade", ForeignKey("habilidades.id"), primary_key=True),
    Column("id_servico", ForeignKey("servicos.id"), primary_key=True),
)


RelacaoTiposServicoServico = Table(
    "relacao_tipos_servico_servico",
    Base.metadata,
    Column("id_tipo_servico", ForeignKey("tipos_servico.id"), primary_key=True),
    Column("id_servico", ForeignKey("servicos.id"), primary_key=True),
)


RelacaoChatMensagens = Table(
    "relacao_chat_mensagens",
    Base.metadata,
    Column("id_chat", ForeignKey("chats.id"), primary_key=True),
    Column("id_mensagem", ForeignKey("mensagens.id"), primary_key=True),
)


RelacaoChatUsuario = Table(
    "relacao_chat_usuario",
    Base.metadata,
    Column("id_chat", ForeignKey("chats.id"), primary_key=True),
    Column("id_usuario", ForeignKey("usuarios.id"), primary_key=True),
)


class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    servicos_criados = relationship("Servico", back_populates="requisitor", foreign_keys="Servico.id_requisitor")
    servicos_prestados = relationship("Servico", back_populates="contribuinte", foreign_keys="Servico.id_contribuinte")
    habilidades = relationship("Habilidade", back_populates="usuarios", secondary=RelacaoUsuarioHabilidade)
    chats = relationship("Chat", secondary=RelacaoChatUsuario, back_populates="participantes")
    mensagens = relationship("Mensagem", back_populates="autor")
    avaliacoes_enviadas = relationship("Avaliacao", back_populates="autor", foreign_keys="Avaliacao.id_autor")
    avaliacoes_recebidas = relationship("Avaliacao", back_populates="avaliado", foreign_keys="Avaliacao.id_avaliado")
    senha = Column(String(255))


class TipoHabilidade(Base):
    __tablename__ = 'tipos_habilidade'
    id = Column(Integer, primary_key=True, index=True)
    habilidades = relationship("Habilidade", back_populates="tipo_habilidade")
    nome = Column(String(100), unique=True)
    cor = Column(String(6), nullable=False)
    icone = Column(String(100), nullable=False)


class Habilidade(Base):
    __tablename__ = "habilidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    id_tipo_habilidade = Column(Integer, ForeignKey("tipos_habilidade.id"))
    tipo_habilidade = relationship("TipoHabilidade", back_populates="habilidades")
    usuarios = relationship("Usuario", secondary=RelacaoUsuarioHabilidade, back_populates="habilidades")
    servicos = relationship("Servico", secondary=RelacaoServicoHabilidade, back_populates="habilidades")


class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150))
    descricao = Column(String(1000))
    id_requisitor = Column(Integer, ForeignKey("usuarios.id"))
    id_contribuinte = Column(Integer, ForeignKey("usuarios.id"))
    requisitor = relationship("Usuario", back_populates="servicos_criados", foreign_keys=[id_requisitor],
                              remote_side="Usuario.id")
    contribuinte = relationship("Usuario", back_populates="servicos_prestados", foreign_keys=[id_contribuinte],
                                remote_side="Usuario.id")
    status = Column(SmallInteger)
    remoto = Column(Boolean)
    habilidades = relationship("Habilidade", secondary=RelacaoServicoHabilidade, back_populates="servicos")
    tipos_servico = relationship("TipoServico", secondary=RelacaoTiposServicoServico, back_populates="servicos")


class TipoServico(Base):
    __tablename__ = "tipos_servico"
    id = Column(Integer, primary_key=True, index=True)
    servicos = relationship("Servico", secondary=RelacaoTiposServicoServico, back_populates="tipos_servico")
    nome = Column(String(100))
    cor = Column(String(6))
    icone = Column(String(100))


class Chat(Base):
    __tablename__ = "chats"
    participantes = relationship("Usuario", secondary=RelacaoChatUsuario, back_populates="chats")
    id = Column(Integer, primary_key=True, index=True)
    id_mensagens = Column(Integer, ForeignKey("mensagens.id"))
    mensagens = relationship("Mensagem", secondary=RelacaoChatMensagens, back_populates="chat")


class Mensagem(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, index=True, primary_key=True)
    id_chat = Column(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", secondary=RelacaoChatMensagens, back_populates="mensagens")
    id_autor = Column(Integer, ForeignKey("usuarios.id"))
    conteudo = Column(String(2048))
    data = Column(DateTime)
    minutos = Column(Integer)
    autor = relationship("Usuario", back_populates="mensagens")


class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    id = Column(Integer, primary_key=True, index=True)
    id_autor = Column(Integer, ForeignKey("usuarios.id"))
    id_avaliado = Column(Integer, ForeignKey("usuarios.id"))
    autor = relationship("Usuario", back_populates="avaliacoes_enviadas", foreign_keys=[id_autor],
                              remote_side="Usuario.id")
    avaliado = relationship("Usuario", back_populates="avaliacoes_recebidas", foreign_keys=[id_avaliado],
                              remote_side="Usuario.id")
    comentario = Column(String(1000))
    pontuacao = Column(Integer)
