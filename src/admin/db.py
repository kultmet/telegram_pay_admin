from datetime import datetime
import typing

from sqlalchemy import Boolean, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    payments: Mapped[typing.List["Payment"]] = relationship("Payment", back_populates="user", cascade='all, delete, delete-orphan')
    blacklist: Mapped[typing.List["BlackList"]] = relationship("BlackList", back_populates="user", cascade='all, delete, delete-orphan')
    total_ballance: Mapped[int] = mapped_column(Integer, default=0)


class Payment(Base):
    __tablename__ = "payment"

    pk = mapped_column(Integer, primary_key=True, autoincrement=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    telegram_payment_charge_id: Mapped[str] = mapped_column(String, nullable=False)
    provider_payment_charge_id: Mapped[str] = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="payments")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)


class BlackList(Base):
    __tablename__ = 'black_list'

    pk: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey("user_account.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="blacklist")
