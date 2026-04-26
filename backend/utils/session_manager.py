# from datetime import datetime
# from sqlmodel import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from models.user_model import UserSession

# async def open_session(db: AsyncSession, user_id: str, ip: str | None = None) -> UserSession:
#     session = UserSession(user_id=user_id, ip_address=ip)
#     db.add(session)
#     await db.commit()
#     await db.refresh(session)
#     return session

# async def close_session(db: AsyncSession, user_id: str) -> None:
#     result = await db.execute(
#         select(UserSession)
#         .where(UserSession.user_id == user_id, UserSession.ended_at == None)
#         .order_by(UserSession.started_at.desc())
#         .limit(1)
#     )
#     active = result.scalars().one_or_none()
#     if active:
#         db.add(active)
#         await db.commit()

# async def get_active_session_id(db: AsyncSession, user_id: str) -> str | None:
#     result = await db.execute(
#         select(UserSession.id)
#         .where(UserSession.user_id == user_id, UserSession.ended_at == None)
#         .order_by(UserSession.started_at.desc())
#         .limit(1)
#     )
#     return result.scalar_one_or_none()