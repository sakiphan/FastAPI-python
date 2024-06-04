from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .database import SessionLocal
from .logs import create_log
from .auth import SECRET_KEY, ALGORITHM  # Gerekli değişkenleri içe aktarın

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        db: Session = SessionLocal()
        ip_address = request.client.host
        endpoint = request.url.path
        method = request.method
        status_code = response.status_code
        user_agent = request.headers.get("user-agent", None)
        username = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("sub")
            except JWTError:
                pass
        create_log(db, ip_address, endpoint, method, status_code, username, user_agent)
        db.close()
        return response