from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.db import BlackList, Payment, User
from src.admin.schemas import (
    BallanceRequest,
    BlackListexistsResponse,
    PaymentRequest,
    PaymentResponse,
    UserExistsResponse,
    UserRequest,
    UserResponse
)
from src.admin.utils import (
    save_blacklist_object, save_payment, save_user, update_ballance
)
from src.database import get_async_session

admin_router = APIRouter()


@admin_router.get(
    path='/users/',
    tags=['Users'],
    response_model=List[UserResponse]
)
async def get_users(session: AsyncSession = Depends(get_async_session)):
    all_users = await session.execute(
        select(
            User.id,
            User.username,
            User.first_name,
            User.is_bot,
            User.language_code,
            User.is_admin,
            User.total_ballance
        )
    )
    return [UserResponse.from_orm(user) for user in all_users.all()]


@admin_router.get(
    path='/users/{user_id}/exists/',
    tags=['Users']
)
async def exists_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        exists(User).where(User.id == user_id).select()
    )
    return UserExistsResponse(exists=result.scalar())


@admin_router.post(
    path='/users/',
    tags=['Users'],
    response_model=UserRequest,
    status_code=201
)
async def create_user(
    user: UserRequest, session: AsyncSession = Depends(get_async_session)
):
    await save_user(session, user)
    return user


@admin_router.get(
    path='/users/{user_id}/payments/',
    tags=['Payments']
)
async def get_user_payments(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    paymens = await session.execute(
        select(User.id, User.username, Payment.total_amount, Payment.timestamp)
        .join(User.payments).where(Payment.user_id == user_id)
    )
    return [PaymentResponse.from_orm(payment) for payment in paymens]


@admin_router.post(
    path='/users/{user_id}/payments/',
    tags=['Payments'],
    status_code=201
)
async def create_payment(user_id: int,
                         payment: PaymentRequest,
                         session: AsyncSession = Depends(get_async_session)):
    await save_payment(session, user_id, payment)
    return payment


@admin_router.patch(
    path='/users/{user_id}/ballance/',
    tags=['Ballance']
)
async def change_ballance(
    user_id: int,
    ballance: BallanceRequest,
    session: AsyncSession = Depends(get_async_session)
):
    await update_ballance(session, user_id, ballance.total_ballance)


@admin_router.post(
    path='/users/{user_id}/blacklist/',
    tags=['Blacklist'],
    status_code=201
)
async def add_to_blacklist(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    await save_blacklist_object(session, user_id)
    return {'message': 'Пользователь заблокирован'}


@admin_router.get(
    path='/users/{user_id}/blacklist/exists/',
    tags=['Blacklist'],
    status_code=201
)
async def exists_blacklist_object(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        exists(BlackList).where(BlackList.user_id == user_id).select()
    )
    return BlackListexistsResponse(exists=result.scalar())


@admin_router.get(
    path='/blacklist/',
    tags=['Blacklist'],
    status_code=200
)
async def get_blacklist(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(BlackList.user_id))
    return result.scalars().all()
