
from sqlalchemy import BigInteger, create_engine, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[BigInteger] = mapped_column()

class Queue(Base):
    __tablename__ = 'queue'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)

class Chats(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True)
    user = mapped_column(BigInteger)
    partner = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)