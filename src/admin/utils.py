from fastapi import HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.db import BlackList, Payment, User
from src.admin.schemas import PaymentRequest, UserRequest

async def save_user(db_session: AsyncSession, user: UserRequest):
    try:
        await db_session.execute(insert(User).values(**user.dict()))
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            403, f'Пользователь {user.id} уже существует.'
        )


async def save_payment(db_session: AsyncSession, user_id: int, paymant: PaymentRequest):
    try:
        ballance = await db_session.execute(select(User.total_ballance).where(User.id==user_id))
        await db_session.execute(insert(Payment).values(user_id=user_id, **paymant.dict()))
        await db_session.execute(update(User).where(User.id == user_id).values(total_ballance=ballance.scalar() + paymant.total_amount))
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            400, f'Bad Request'
        )


async def update_ballance(db_session: AsyncSession, user_id: int, total_ballance):
    try:
        await db_session.execute(update(User).where(User.id == user_id).values(total_ballance=total_ballance))
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            400, f'Bad Request'
        )


async def save_blacklist_object(db_session: AsyncSession, user_id: UserRequest):
    try:
        await db_session.execute(insert(BlackList).values(user_id=user_id))
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            403, f'Пользователь уже в забокинован.'
        )