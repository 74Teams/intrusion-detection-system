from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import SETTINGS
from services.database.models import Base

db_url = SETTINGS.get("database", {}).get("db_url", "sqlite:///./nids_events.db")

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Khởi tạo toàn bộ bảng trong cơ sở dữ liệu nếu chưa tồn tại."""
    Base.metadata.create_all(bind=engine)
