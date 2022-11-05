class UsuarioException(Exception):
    ...


class UsuarioNotFoundError(UsuarioException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Usuário não encontrado"


class UsuarioAlreadyExistError(UsuarioException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Usuário já cadastrado"


class TipoHabilidadeException(Exception):
    ...


class TipoHabilidadeAlreadyExistsError(TipoHabilidadeException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Tipo de Habilidade já existente"


class TipoHabilidadeNotFoundError(TipoHabilidadeException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Tipo de habilidade não encontrado"


class HabilidadeException(Exception):
    ...


class HabilidadeAlreadyExistsError(HabilidadeException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Habilidade já existente"


class HabilidadeNotFoundError(HabilidadeException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Habilidade não encontrado"


class TipoServicoException(Exception):
    ...


class TipoServicoAlreadyExistsError(TipoServicoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Tipo de serviço já existente"


class TipoServicoNotFoundError(TipoServicoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Tipo de serviço não encontrado"


class ServicoException(Exception):
    ...


class ServicoAlreadyExistsError(ServicoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Serviço já existente"


class ServicoNotFoundError(ServicoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Serviço não encontrado"


class MensagemException(Exception):
    ...


class MensagemAlreadyExistsError(MensagemException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Mensagem já existente"


class MensagemNotFoundError(MensagemException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Mensagem não encontrada"


class AvaliacaoException(Exception):
    ...


class AvaliacaoAlreadyExistsError(AvaliacaoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Avaliação já existente"


class AvaliacaoNotFoundError(AvaliacaoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Avaliação não encontrada"


class ChatException(Exception):
    ...


class ChatAlreadyExistsError(ChatException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Chat já existente"


class ChatNotFound(ChatException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Chat não encontrado"


