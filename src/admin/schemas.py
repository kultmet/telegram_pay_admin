from datetime import datetime

from pydantic import BaseModel


class UserRequest(BaseModel):
    id: int
    is_bot: bool
    first_name: str = None
    username: str = None
    language_code: str


class UserResponse(UserRequest):
    is_admin: bool
    total_ballance: int

    class Config:
        orm_mode = True


class PaymentRequest(BaseModel):
    currency: str
    total_amount: int
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class PaymentResponse(BaseModel):
    id: int
    username: str
    total_amount: int
    timestamp: datetime

    class Config:
        orm_mode = True


class UserExistsResponse(BaseModel):
    exists: bool


class BallanceRequest(BaseModel):
    total_ballance: int = None


class BlackListexistsResponse(UserExistsResponse):
    pass
