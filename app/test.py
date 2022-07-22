import os

from db.database import Base
from main import *

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

import os


load_dotenv()

SQLALCHEMY_DATABASE_URL = 'postgresql://' + \
    os.getenv('PG_USER') + ':' + os.getenv('PG_PASSWORD') +\
        '@' + os.getenv('PG_HOSTNAME') + ':' + os.getenv('PG_PORT') + '/' + os.getenv('PG_DBNAME')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db(): 
    try: 
        db = TestingSessionLocal() 
        yield db 
    finally: 
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_is_dotenv_work():
    from dotenv import load_dotenv


    load_dotenv()

    pgadmin_dbname = os.getenv('PG_DBNAME')

    assert 'fastapiserverpostgresqldb' == pgadmin_dbname

def test_read_root():
    response = client.get('/')
    
    assert 200 == response.status_code
    assert {"Hello":"World"} == response.json()

def test_db():
    response = client.get('/users/1')

    assert 200 == response.status_code
    assert {"email":"testemail@test.com","id":1,"is_active":True} == response.json()
