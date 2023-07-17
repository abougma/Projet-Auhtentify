from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
import hashlib
import requests


Base = declarative_base()
app = FastAPI()

# Creation de la classe
class user(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    pseudo = Column(String(32), unique=True)
    password = Column(String(32))
    last_connection_date = Column(String(10))

# Modèles Pydantic pour la création et la récupération d'un utilisateur
class UserIn(BaseModel):
    pseudo: str
    password: str

class UserOut(BaseModel):
    message: str

# Connexion avec la base de donnee
engine = create_engine('mysql+pymysql://root:Lemonde2020@localhost:3308/projetams')
Base.metadata.create_all(engine)
# Créer une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

#Fonction permettant de verifier qu'utilisateur exsiste dans la base de donnee
def verify_credentials(pseudo: str, password: str):
    try:
        # Hasher le mot de passe
        password_hash = hashlib.md5(password.encode()).hexdigest()
        # Recherche de l'utilisateur par son nom d'utilisateur et le mot de passe
        std = session.query(user).filter_by(pseudo=pseudo, password=password_hash).first()
        if std is not None:
            std.last_connection_date = datetime.now()
            session.commit()
            return std.id
        else:
            return -1
    except Exception as erreur:
        # Une erreur imprévue est survenue
        session.rollback()  
        raise erreur


#Fonction permettant de creer un utilisateur
def register_user(pseudo: str, password: str):
    try:
        # Hasher le mot de passe
        password_hash = hashlib.md5(password.encode()).hexdigest()
        # Recherche de l'utilisateur par son nom d'utilisateur et le mot de passe
        std = session.query(user).filter_by(pseudo=pseudo, password=password_hash).first()
        if std:
            raise ValueError("le pseudo exsiste deja ")
        new_user = user(pseudo=pseudo, password=password_hash, last_connection_date=datetime.now())
        session.add(new_user)
        session.commit()
        return UserOut(message="Utilisateur créé avec succès")
    # L'utilisateur exsiste deja dans la base de données
    except ValueError as erreur:
        return UserOut(message=str(erreur))
    except Exception as erreur:
        session.rollback()
        raise erreur

#Pour creer un nouvel utilisateur
@app.post("/register", response_model=UserOut)
async def create_user(user: UserIn):
    result = register_user(user.pseudo, user.password)
    if result.message != "Utilisateur créé avec succès":
        raise HTTPException(status_code=400, detail=result.message)
    return result


#Pour se connecter a l'aide de nos identifiant

@app.post("/login", response_model=UserOut)
async def login(user: UserIn):
    std = verify_credentials(user.pseudo, user.password)
    if std != -1:
        return UserOut(message="Connexion reussie")
    else:
        raise HTTPException(status_code=403, detail="Invalid username or password")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


