from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Optional
from typing import List


class Base(AsyncAttrs, DeclarativeBase):
    pass


class MessageID(Base):
    __tablename__ = 'chat_history'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    user_id: Mapped[int]
    message_id: Mapped[int]


class Rights(Base):
    __tablename__ = 'rights'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    user_id: Mapped[str] = mapped_column(String(100))
    user_rights: Mapped[str] = mapped_column(String(20))


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    post_type: Mapped[str] = mapped_column(String(5))
    from_user: Mapped[str] = mapped_column(String(40))
    text: Mapped[Optional[str]] = mapped_column(String(2000))
    date: Mapped[datetime] = mapped_column(insert_default=func.now())
    media: Mapped[List["Media"]] = relationship(cascade='all, delete')


class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    file_id: Mapped[Optional[str]] = mapped_column(String(100))
    file_type: Mapped[Optional[str]] = mapped_column(String(100))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))


class DeleteButton(Base):
    __tablename__ = 'delete_buttons'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    user_id: Mapped[int]
    keyboard_id: Mapped[int]
    post_id: Mapped[int]
    messages_id: Mapped[str] = mapped_column(String(100))
