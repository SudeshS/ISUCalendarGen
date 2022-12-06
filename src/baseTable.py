import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv


load_dotenv()
db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url, pool_size=5, max_overflow=0, echo=False, pool_reset_on_return='commit')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.drop_all(engine)
