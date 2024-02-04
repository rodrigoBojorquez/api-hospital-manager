from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# OAUTH2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="public/token")

# PASSLIB
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JOSE
SECRET_KEY = "f943049c4ecca5819192981f721c21c31b8ad2897d93885c1b28ff446db71421"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120