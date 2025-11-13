import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional, List
from ..domain.user_entities import User, CasoClinicoHistorico

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    token = Column(String(500))
    token_expires_at = Column(DateTime)

class ClinicalCaseModel(Base):
    __tablename__ = "clinical_cases"
    
    id = Column(String, primary_key=True)  # UUID
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    ap_hi = Column(Integer, nullable=False)
    ap_lo = Column(Integer, nullable=False)
    cholesterol = Column(Integer, nullable=False)
    gluc = Column(Integer, nullable=False)
    smoke = Column(Integer, nullable=False)
    alco = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    correct_risk = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CasoHistoricoModel(Base):
    __tablename__ = "casos_historico"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    caso_dados = Column(Text, nullable=False)
    gabarito = Column(String(50), nullable=False)
    resposta_usuario = Column(String(50), nullable=False)
    acertou = Column(Boolean, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

class PostgresUserRepository:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cardio_ml_db")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def create_user(self, login: str, nome: str, senha_hash: str) -> Optional[User]:
        try:
            user_model = UserModel(login=login, nome=nome, senha_hash=senha_hash)
            self.session.add(user_model)
            self.session.commit()
            return User(user_model.id, login, nome, senha_hash)
        except:
            self.session.rollback()
            return None
    
    def get_user_by_login(self, login: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(login=login).first()
        if user_model:
            return User(user_model.id, user_model.login, user_model.nome, user_model.senha_hash)
        return None
    
    def save_token(self, user_id: int, token: str, expires_at: datetime) -> None:
        user_model = self.session.query(UserModel).filter_by(id=user_id).first()
        if user_model:
            user_model.token = token
            user_model.token_expires_at = expires_at
            self.session.commit()
    
    def verify_token(self, token: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(token=token).first()
        if user_model and user_model.token_expires_at and user_model.token_expires_at > datetime.utcnow():
            return User(user_model.id, user_model.login, user_model.nome, user_model.senha_hash)
        return None
    
    def save_caso_historico(self, user_id: int, caso_dados: dict, gabarito: str, 
                           resposta: str, acertou: bool) -> None:
        try:
            historico_model = CasoHistoricoModel(
                user_id=user_id,
                caso_dados=str(caso_dados),
                gabarito=gabarito,
                resposta_usuario=resposta,
                acertou=acertou
            )
            self.session.add(historico_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_historico_user(self, user_id: int) -> List[dict]:
        casos = self.session.query(CasoHistoricoModel).filter_by(user_id=user_id).order_by(CasoHistoricoModel.data.desc()).all()
        
        return [{
            "caso_dados": eval(caso.caso_dados),
            "gabarito": caso.gabarito,
            "resposta": caso.resposta_usuario,
            "acertou": caso.acertou,
            "data": caso.data.isoformat()
        } for caso in casos]
    
    def delete_user(self, user_id: int) -> None:
        # Deletar histórico de casos
        self.session.query(CasoHistoricoModel).filter_by(user_id=user_id).delete()
        # Deletar usuário
        self.session.query(UserModel).filter_by(id=user_id).delete()
        self.session.commit()