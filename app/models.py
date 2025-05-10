from sqlalchemy import Table, Column, Integer, String
from app.database import metadata

pipelines = Table(
    "pipelines",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("repo_url", String),  # например "glebus-sasha/demotwo"
)
