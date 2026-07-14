#CONNECTING TO THE DATABASE

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#"postgresql://username:password@localhost/dbname"
db_url = "postgresql://postgres:1234@localhost:5432/fastapi_db"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)