from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgresql:S1g2m2@pri@localhost/fastapi'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

seession = sessionmaker(autocommit = False,autoflush= False,bind=engine)