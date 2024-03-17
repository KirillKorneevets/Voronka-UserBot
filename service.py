import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from models import UserStatusEnum
from sqlalchemy.exc import IntegrityError


async def add_user(user_id: int, session: AsyncSession):
    try:    
        now = datetime.datetime.now()
        user = User(id=user_id, created_at=now, status=UserStatusEnum.ALIVE, status_updated_at=now)
        session.add(user)
        await session.commit()
    except IntegrityError:
        print(f"Пользователь {user_id} уже существует.")
        await session.rollback()


async def user_status_finished(user_id: int, session: AsyncSession):
    now = datetime.datetime.now()
    await session.execute(update(User).where(User.id == user_id).values(status=UserStatusEnum.FINISHED, status_updated_at=now))
    await session.commit()
 

async def user_status_dead (user_id: int, session: AsyncSession):
    now = datetime.datetime.now()
    await session.execute(update(User).where(User.id == user_id).values(status=UserStatusEnum.DEAD, status_updated_at=now))
    await session.commit()


async def listen_for_message(message):
    while True:
        text_message = message.text
        if text_message:
            return text_message


