# @File : database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH=r"C:\Users\qwrdxer\Desktop\AcadeAgent\res\AcadeAgent\database.db"
print(DB_PATH)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# 来允许SQLite这样
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 用于建立数据库SQLAlchemy模型models
Base = declarative_base()