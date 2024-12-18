import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from shema_api.rout import contacts, auth, ava, email, reset
from shema_api.data.base import engine
from shema_api.mod import models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Создание таблиц БД
models.Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()

# CORS middleware
origins = [
    "http://localhost:3000",
    "https://example.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(contacts.router, tags=["contacts"])
app.include_router(auth.router, tags=["auth"])
app.include_router(ava.router, tags=["auth"])
app.include_router(email.router, tags=["email"])
app.include_router(reset.router, tags=["password-reset"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_token(token: str = Depends(oauth2_scheme)):
    if token != "some_token":  # This is just a mock validation, adjust to your logic
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return token
# Пример с ограничением запросов
@app.get("/limited")
async def limited_endpoint(token: str = Depends(get_token)):
    return {"message": "This endpoint is rate limited to 5 requests per minute."}


# Пример без ограничения запросов
@app.get("/unlimited", tags=["rate limiting"])
async def unlimited_endpoint():
    """Function unlimited_endpoint printing python version."""
    return {"message": "This endpoint has no rate limiting."}

redis_url = "redis://localhost:6379"  # Adjust this to your Redis URL
redis = redis.from_url(redis_url)

@app.on_event("startup")
async def startup():
    # Инициализация FastAPILimiter с нужными параметрами, например, подключение к Redis
    await FastAPILimiter.init(redis)

# Точка входа для запуска приложения
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
