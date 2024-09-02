from data.models import Queue, Chats, User
from data.models import async_session
from sqlalchemy import select

async def add_queue(user_id):
    async with async_session() as session:

        queue = Queue(user_id=user_id)
        session.add(queue)
        await session.commit()

async def delete_queue(user_id):
        async with async_session() as session:
            queue = await session.scalar(select(Queue).where(Queue.user_id == user_id))
            if queue:
                await session.delete(queue)
                await session.commit()

async def get_queue():
        async with async_session() as session:
            queue = await session.scalar(select(Queue))
            if queue:
                return queue.user_id
            else:
                return False

async def create_chat(user_id, partner_id):
        async with async_session() as session:
            if partner_id != 0:
                chat = Chats(user=user_id, partner=partner_id)
                session.add(chat)
                await session.commit()
                return True
            return False

async def get_chat(user_id):
        async with async_session() as session:
            chat = await session.scalar(select(Chats).filter((Chats.user == user_id) | (Chats.partner == user_id)))
            if chat:
                return [chat.id, chat.user if chat.user != user_id else chat.partner]
            else:
                return False

async def delete_chat(user_id):
        async with async_session() as session:
            chat = await session.scalar(select(Chats).filter((Chats.user == user_id) | (Chats.partner == user_id)))
            if chat:
                await session.delete(chat)
                await session.commit()


async def set_user(user_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.user_id == user_id))
            
            if not user:
                user = User(user_id=user_id)
                session.add(user)
                await session.commit()
                return True