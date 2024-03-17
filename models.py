from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, MetaData
from db_config import AsyncBase
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from enum import Enum

metadata = MetaData()

class UserStatusEnum(Enum):
    ALIVE = 'alive'
    DEAD = 'dead'
    FINISHED = 'finished'


class User(AsyncBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(PgEnum(UserStatusEnum, name='user_status_enum' ), default=UserStatusEnum.ALIVE)
    status_updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))



