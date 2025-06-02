from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database.config import db_settings

#todo что такое scoped_session
class DataBase:
    engine = create_async_engine(db_settings.get_db_url)
    session = async_sessionmaker(engine, expire_on_commit=False)

