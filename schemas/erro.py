from pydantic import BaseModel


class ErroSchema(BaseModel):
    """ Mensagem de erro será uma string
    """
    mensagem: str