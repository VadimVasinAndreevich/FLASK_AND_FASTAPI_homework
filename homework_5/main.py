"""
Необходимо создать API для управления списком задач.
Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
Для этого использовать библиотеку Pydantic.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from fastapi.responses import HTMLResponse

app = FastAPI()


class Task(BaseModel):
    id: Optional[int]
    title: str = 'название задачи'
    description: str = 'описание задачи'
    status: str = 'не выполнена' or bool


tasks = []


@app.get('/', response_class=HTMLResponse)
async def line():
    return "<a href='/docs'>.....Автодок.....</a>"


@app.get('/tasks', response_model=List[Task])
async def read_tasks():
    return tasks


@app.get('/read_tasks/{task_id}', response_model=Task)
async def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="task not found")


@app.post('/new_tasks', response_model=Task)
async def create_task(task: Task):
    old_id = tasks[-1].id if tasks else 0
    task.id = old_id + 1
    tasks.append(task)
    return task


@app.put('/update_tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, task_ in enumerate(tasks):
        if task_id == task_.id:
            tasks[i] = task
            return task
    raise HTTPException(status_code=404, detail="task not found")


@app.put('/update_status_tasks/{task_id}', response_model=Task)
async def update_task(task_id: int):
    for task in tasks:
        if task_id == task.id:
            if task.status == 'не выполнена':
                task.status = 'выполнена'
            return task
    raise HTTPException(status_code=404, detail="task not found")


@app.delete('/delete_tasks/{task_id}', response_model=Task)
async def delete_task(task_id: int):
    for i, task_ in enumerate(tasks):
        if task_id == task_.id:
            tasks[i].status = False
            return {'msg': 'all done'}
    raise HTTPException(status_code=404, detail="task not found")
