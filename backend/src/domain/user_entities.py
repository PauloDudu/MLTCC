from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    login: str
    nome: str
    senha_hash: str

@dataclass
class CasoClinicoHistorico:
    id: Optional[int]
    user_id: int
    caso_dados: dict
    gabarito: str
    resposta_usuario: str
    acertou: bool
    data: datetime