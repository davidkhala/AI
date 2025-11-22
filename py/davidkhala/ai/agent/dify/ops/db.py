from davidkhala.data.base.pg import Postgres


class DB(Postgres):

    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self.connect()
    def get_dict(self, sql): return self.query(sql).mappings().all()

    @property
    def accounts(self): return self.get_dict("select name, email from accounts where status = 'active'")

    @property
    def apps(self): return self.get_dict("select id, name, mode from apps where status = 'normal'")

