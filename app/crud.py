from app.models import pipelines
from app.database import database

async def create_pipeline(name: str, repo_url: str):
    query = pipelines.insert().values(name=name, repo_url=repo_url)
    pipeline_id = await database.execute(query)  # Выполняем вставку и получаем ID нового пайплайна
    return pipeline_id

# Функция для удаления пайплайна по ID
async def delete_pipeline(pipeline_id: int):
    query = pipelines.delete().where(pipelines.c.id == pipeline_id)
    result = await database.execute(query)
    return result  # Если пайплайн был удален, результат будет > 0

# Функция для получения всех пайплайнов
async def get_all_pipelines():
    query = pipelines.select()
    return await database.fetch_all(query)

# Функция для получения пайплайна по ID
async def get_pipeline_by_id(pipeline_id: int):
    query = pipelines.select().where(pipelines.c.id == pipeline_id)
    return await database.fetch_one(query)