from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.database import database
from pydantic import BaseModel
from app.models import pipelines
import subprocess
from app import crud  # Явный импорт модуля crud
from fastapi.staticfiles import StaticFiles
import os  # Добавляем этот импорт
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешаем доступ с фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/pipelines")
async def list_pipelines():
    pipelines = await crud.get_all_pipelines()
    return pipelines

@app.get("/pipelines/{pipeline_id}")
async def get_pipeline(pipeline_id: int):
    pipeline = await crud.get_pipeline_by_id(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@app.post("/run/{pipeline_id}")
async def run_pipeline(pipeline_id: int):
    query = pipelines.select().where(pipelines.c.id == pipeline_id)
    pipeline = await database.fetch_one(query)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    result = subprocess.run(
        ["nextflow", "run", pipeline["repo_url"]],
        capture_output=True,
        text=True
    )
    return {
        "pipeline": pipeline["name"],
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

# Модель для ввода данных пайплайна
class PipelineCreate(BaseModel):
    name: str
    repo_url: str

@app.post("/pipelines/")
async def add_pipeline(pipeline: PipelineCreate):
    try:
        # Вызов функции из модуля crud
        pipeline_id = await crud.create_pipeline(pipeline.name, pipeline.repo_url)
        return {"id": pipeline_id, "name": pipeline.name, "repo_url": pipeline.repo_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка добавления пайплайна: {str(e)}")


@app.delete("/pipelines/{pipeline_id}")
async def delete_pipeline(pipeline_id: int):
    try:
        # Попытаться удалить пайплайн
        result = await crud.delete_pipeline(pipeline_id)
        if result == 0:  # Если пайплайн не был найден
            raise HTTPException(status_code=404, detail="Pipeline not found")
        return {"detail": "Pipeline deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка удаления пайплайна: {str(e)}")
    
# Подключаем React-сборку как статику
app.mount("/static", StaticFiles(directory="/frontend/build/static"), name="static")

# Главная страница отдаёт index.html
@app.get("/")
def read_index():
    index_path = os.path.join("frontend", "build", "index.html")
    return FileResponse(index_path)
