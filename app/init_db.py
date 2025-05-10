from sqlalchemy import create_engine
from app.database import metadata, DATABASE_URL
from app.models import pipelines

engine = create_engine(str(DATABASE_URL).replace('+asyncpg', ''))
metadata.create_all(engine)

print("Таблицы успешно созданы!")
