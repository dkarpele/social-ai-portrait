import uuid
import datetime

from sqlalchemy import Column, DateTime, String, Boolean, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from db.db_sql import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    tg_chat_id = Column(BigInteger, unique=True, nullable=False)
    tg_first_name = Column(String(50))
    tg_last_name = Column(String(50))
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime,
                        default=datetime.datetime.utcnow)
    modified_at = Column(DateTime,
                         default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)

    def __init__(self,
                 tg_chat_id: int,
                 tg_first_name: str = None,
                 tg_last_name: str = None,
                 disabled: bool = False,
                 ) -> None:
        self.tg_chat_id = tg_chat_id
        self.tg_first_name = tg_first_name if tg_first_name else ""
        self.tg_last_name = tg_last_name if tg_last_name else ""
        self.disabled = disabled

    def __repr__(self) -> str:
        return (f'<User {self.tg_chat_id=} {self.tg_first_name=} '
                f'{self.tg_last_name=}>')
