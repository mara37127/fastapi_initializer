from contextvars import ContextVar
import os
from playhouse.db_url import connect
import peewee


db_state_default = {"closed": None, "conn": None,
                    "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


# for container
# please comment this section if you are not using container
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_HOST = os.getenv("MYSQL_HOST")
db = connect(f'mysql://{MYSQL_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}')


# for local
# please uncomment this section if you are using local database
#db = connect('mysql://root:root@localhost:3306/test')


db._state = PeeweeConnectionState()
