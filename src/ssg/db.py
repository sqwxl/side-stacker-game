import sqlite3
from pathlib import Path
from typing import cast

from quart import Quart


def connect_db(app: Quart) -> sqlite3.Connection:
    conn = sqlite3.connect(cast(Path, app.config["DATABASE"]))
    conn.row_factory = sqlite3.Row
    return conn
