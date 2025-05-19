from .run import app, run, init_db as _init_db


def init_db():
    return _init_db(app)


__all__ = ["app", "run", "init_db"]
