from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from configs.db import get_session
from models.models import User,Task, UserRole
from schemas.tasks import TaskBase, TaskUpdate
from utils.token.token_auth import get_current_user
from auth.roles_dependencies import (
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

@task_router.put("/update/{task_id}")
async def update_task(
    task_id: str,
    request: TaskUpdate,
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

    if request.title is not None:
        task.title = request.title

    if request.description is not None:
        task.description = request.description

    if request.status is not None:
        task.status = request.status

    if request.priority is not None:
        task.priority = request.priority

    if request.deadline is not None:
        task.deadline = request.deadline
        

    await session.commit()
    await session.refresh(task)

    return {
        "msg": "Task updated successfully",
        "task": task
    }

@task_router.delete("/delete/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Task).where(Task.id == task_id) # type: ignore
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    check_self_or_roles(
        user=current_user,
        resource_user_id=task.created_by,
        allowed_roles=[UserRole.ADMIN]
    )
    
    await session.delete(task)
    await session.commit()

    return {
        "msg": "Task deleted successfully"
    }