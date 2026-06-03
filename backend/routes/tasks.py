from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from configs.db import get_session
from models.models import User,Task, UserRole
from schemas.tasks import TaskBase
from utils.token.token_auth import get_current_user
from utils.roles_dependencies import (
    AdminOnly,
    AdminOrManager,
    check_self_or_roles
)

task_router = APIRouter(prefix='/task', tags=["Task"])

@task_router.post("/create")
async def create_task(
    request: TaskBase,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    print(request)
    data = {}
    new_task = Task(
        title= request.title,
        description = request.description,
        status= request.status,
        priority= request.priority,
        created_by= current_user.id,
        deadline= request.deadline,
    )
    
    session.add(new_task)
    try:
        await session.commit()
        await session.refresh(new_task)
    except IntegrityError:
        await session.rollback()
        data["msg"] = "Task creation failed"
        return data
    data['msg'] = "Task Created Successfully"
    return data
    
@task_router.get("/get-all-users")
async def get_all_possible_task(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found!")
    return tasks



@task_router.get("/get/{task_id}")
async def get_(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Task).where(Task.id == task_id) # type: ignore
    )
    task = result.scalars().one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    check_self_or_roles(
        user=current_user,
        resource_user_id=task.created_by,
        allowed_roles=[UserRole.ADMIN]
    )

    return task

# @task_router.put("/update/{user_id}")
# async def update_user(
#     user_id: str,
#     request: UserUpdate,
#     current_user: User = SelfOrAdmin,
#     session: AsyncSession = Depends(get_session)
# ):
#     data ={}
#     result = await session.execute(
#         select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
#     )
#     user = result.scalars().one_or_none()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if request.name is not None:
#         user.name = request.name

#     if request.email is not None:
#         user.email = request.email

#     await session.commit()
#     await session.refresh(user)
#     data["msg"] = "User updated successfully"
#     data["user"] = user
#     return data

# @task_router.delete("/delete/{user_id}")
# async def delete_user(
#     user_id: str,
#     current_user: User = AdminOrManager,
#     session: AsyncSession = Depends(get_session)
# ):
#     data = {}
#     result = await session.execute(
#         select(User).where(User.id == user_id) # pyright: ignore[reportArgumentType]
#     )
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if user.id == current_user.id:
#         raise HTTPException(status_code=400, detail="Cannot delete yourself")

#     await session.delete(user)
#     await session.commit()
    
#     data["msg"] = "User deleted successfully"
#     return data