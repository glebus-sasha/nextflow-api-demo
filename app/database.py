from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql+asyncpg://fastapi:secret@db:5432/nextflow_db"

database = Database(DATABASE_URL)
metadata = MetaData()
