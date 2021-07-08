from fastapi import FastAPI
from databases import Database # to establish connection to postgresql with the db url string in config.py
from app.core.config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    database = Database(DATABASE_URL, min_size=2, max_size=10) # minimum and maximum number of connections at given time, can be also added to config.py

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ----")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ----")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")