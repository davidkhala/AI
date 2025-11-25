from typing import Any, Optional, Dict

from davidkhala.data.base.pg import Postgres
from sqlalchemy import desc
from sqlalchemy.orm import Session

from davidkhala.ai.agent.dify.ops.db.orm import AppModelConfig


class DB(Postgres):

    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self.connect()

    def get_dict(self,
                 template: str,
                 values: Dict[str, Any] | None = None,
                 request_options: Dict[str, Any] | None = None
                 ) -> list[dict]:
        return Postgres.rows_to_dicts(self.query(template, values, request_options))

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

    def update_app_config(self, record: AppModelConfig, refresh: bool = False) -> AppModelConfig | None:
        with Session(self.client) as session:
            session.add(record)
            session.commit()
            if refresh:
                session.refresh(record)  # 刷新对象，确保拿到数据库生成的字段（如 id）
                return record
            return None

    def hit_run(self, top_k: int = 3):
        template = "SELECT dataset_id, document_id, content FROM document_segments ORDER BY hit_count DESC LIMIT :top_k"
        return self.get_dict(template, {'top_k': top_k})

    def dataset_queries(self, dataset_id, limit=20) -> list[str]:
        template = "select content from dataset_queries where source = 'app' and created_by_role = 'end_user' and dataset_id = :dataset_id limit :limit"
        return self.query(template, {'dataset_id': dataset_id, 'limit':limit}).scalars().all()
