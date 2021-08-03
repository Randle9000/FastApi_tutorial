from databases import Database


class BaseRepository:
    def __init__(self, db: Database) -> None:
        # to keep reference to the connection to db
        self.db = db
