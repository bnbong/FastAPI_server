import os

from db.database import Base
from main import *

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

import os
import hashlib


load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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

def hashing_text():
    test_password = "thepasswordtext"
    test_text = test_password + "thiswillbehashed"
    test_text = test_text.encode()
    h = hashlib.sha256()
    h.update(test_text)
    hashed_text = h.hexdigest()

    return hashed_text

def reverting_changing(client, url, json_text):
    client.put(url, json=json_text)

def test_is_dotenv_work():
    from dotenv import load_dotenv


    load_dotenv()

    pgadmin_dbname = os.getenv('PG_DBNAME')

    assert 'fastapiserverpostgresqldb' == pgadmin_dbname

def test_is_hashing_function_work():
    test_text = "thepasswordtext" + "thiswillbehashed"
    hashed_text = hashing_text()
    
    assert not hashed_text == test_text

def test_read_root():
    response = client.get('/')
    
    assert 200 == response.status_code
    assert {"Hello":"World"} == response.json()

def test_get_all_users():
    response = client.get('/users')

    assert 200 == response.status_code
    if response.json() != []:
        assert [{'email': 'test@testmail.com', 'id': 1, 'is_active': True}] == response.json()

def test_make_user_at_db():
    response_check_users = client.get('/users')
    response = client.post('/users/', json={"email":"test@testmail.com", "password":"testpw"})

    if response_check_users.json() == []:
        assert 200 == response.status_code
        assert {"email":"test@testmail.com","id":1,"is_active":True} == response.json()

    else:
        assert 400 == response.status_code
        assert {'detail': 'Email already registered'} == response.json()

def test_db():
    response = client.get('/users/1')

    assert 200 == response.status_code
    assert {"email":"test@testmail.com","id":1,"is_active":True} == response.json()

def test_user_info_change():
    response = client.put('/users/1', json={"email":"test@testmail.com","is_active":False})

    assert 200 == response.status_code
    assert {"email":"test@testmail.com","id":1,"is_active":False} == response.json()

    if response.json()["is_active"] == False:
        reverting_changing(client=client, url="/users/1", json_text={"email":"test@testmail.com","is_active":True})

def test_user_password_change():
    unchanged_password = TestingSessionLocal().query(models.User).first().hashed_password
    response = client.put("/users/changepw/1", json={"email":"test@testmail.com","password":"newpassword"})

    assert 200 == response.status_code
    changed_password = TestingSessionLocal().query(models.User).first().hashed_password

    assert unchanged_password != changed_password

    reverting_changing(client=client, url="/users/changepw/1", json_text={"email":"test@testmail.com","password":"testpw"})
