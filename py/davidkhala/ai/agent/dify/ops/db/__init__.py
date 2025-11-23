from typing import Any, Optional

from davidkhala.data.base.pg import Postgres
from sqlalchemy import desc
from sqlalchemy.orm import Session

from davidkhala.ai.agent.dify.ops.db.orm import AppModelConfig


class DB(Postgres):

    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self.connect()

    def get_dict(self, sql): return self.query(sql).mappings().all()

    @property
    def accounts(self): return self.get_dict("select name, email from accounts where status = 'active'")

    @property
    def apps(self): return self.get_dict("select id, name, mode from apps where status = 'normal'")

    def app_config(self, app_id) -> AppModelConfig | None:
        with Session(self.client) as session:
            return (
                session.query(AppModelConfig)
                .filter(AppModelConfig.app_id == app_id)
                .order_by(desc(AppModelConfig.created_at))
                .first()
            )

    def update_app_config(self, record: AppModelConfig, refresh:bool=False) -> AppModelConfig | None:
        with Session(self.client) as session:
            session.add(record)
            session.commit()
            if refresh:
                session.refresh(record)  # 刷新对象，确保拿到数据库生成的字段（如 id）
                return record
            return None
