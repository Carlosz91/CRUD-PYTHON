# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .. import schemas, models, database, auth

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# ----------------------------
# Dependencia para JWT
# ----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Helper para obtener el usuario actual a partir del JWT.
    """
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        # ✅ Convertir de string a int
        user_id = int(user_id_str)
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except ValueError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return user

# ----------------------------
# Registro de usuario
# ----------------------------
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    
    """
    Registrar un nuevo usuario.
    Hashea la contraseña y guarda en la BD.
    """
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# ----------------------------
# Login
# ----------------------------
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Login de usuario.
    Verifica contraseña y devuelve JWT.
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    # ✅ Convertir user.id a string
    access_token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

