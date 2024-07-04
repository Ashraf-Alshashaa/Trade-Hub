from . import *
from dotenv import dotenv_values
from db import db_user
from db.models import DbUser, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
config = dotenv_values(".env")
SECRET_KEY = config["SECRET_KEY"]
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']
ALGORITHM = config['ALGORITHM']


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db_user.get_user_by_username(db, username)

    if user is None:
        raise credentials_exception

    return user


def optional_get_current_user(request: Request, db: Session = Depends(get_db)):
    token: Optional[str] = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        return DbUser(
            id=0,
            username="guest",
            email="guest@example.com",
            password="",
            role=UserRole.USER,
            address=[],
            products_selling=[],
            products_buying=[],
            bids=[],
            payments=[]
        )
    
    token = token[len("Bearer "):]
    
    try:
        return get_current_user(token, db)
    except HTTPException:
        return DbUser(
            id=0,
            username="guest",
            email="guest@example.com",
            password="",
            role=UserRole.USER,
            address=[],
            products_selling=[],
            products_buying=[],
            bids=[],
            payments=[]
        )