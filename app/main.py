import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas, crud, database, auth, logs
from .middleware import LoggingMiddleware

# Logging yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Veritabanı bağlantısı ve modeller
models.Base.metadata.create_all(bind=database.engine)
logs.Base.metadata.create_all(bind=database.engine)

# Uygulama oluşturma
app = FastAPI()

# CORS Orta Katmanını Ekleme
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware ekleme
app.add_middleware(LoggingMiddleware)

# Ana sayfa endpoint'i
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Vision Football API"}

# Kayıt endpoint'i
@app.post("/register/", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    logger.info(f"Registering user: {user.username}")
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    db_user = crud.create_user(db, user)
    return db_user

# Giriş endpoint'i
@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    logger.info(f"Logging in user: {form_data.username}")
    user = crud.get_user(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    logger.info(f"User {form_data.username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

# Kullanıcı bilgileri endpoint'i
@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    logger.info(f"Fetching details for user: {current_user.username}")
    return current_user

# Çıkış endpoint'i
@app.post("/logout")
async def logout(token: str = Depends(auth.oauth2_scheme)):
    logger.info("Logging out user")
    auth.blocklist.add(token)
    return {"message": "Successfully logged out"}

# Kullanıcı silme endpoint'i
@app.delete("/users/me", response_model=dict)
async def delete_user(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    logger.info(f"Deleting user with ID: {current_user.id}")
    user_deleted = crud.delete_user(db, current_user.id)
    if not user_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
