from sqlmodel import SQLModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

# print("os.getenv('DB_USERNAME') =", os.getenv("DB_USERNAME")) 
# print("os.getenv('DB_PASSWORD') =", os.getenv("DB_PASSWORD"))
# print("os.getenv('DB_NAME') =", os.getenv("DB_NAME"))
# print("os.getenv('DB_PORT') =", os.getenv("DB_PORT"))
# print("os.getenv('DB_HOST') =", os.getenv("DB_HOST"))
# print("Environment variables loaded successfully.")


username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
dbname = os.getenv("POSTGRES_DB")
db_port = os.getenv("POSTGRES_PORT")
db_host = os.getenv("POSTGRES_HOST")



DATABASE_URL = (
    f"postgresql+asyncpg://{username}:{password}@{db_host}:{db_port}/{dbname}"
)

print("DATABASE_URL =", DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session









# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise RuntimeError("DATABASE_URL is not set")

# print("DATABASE_URL =", DATABASE_URL)
# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
