import os
import unittest

from db.database import Base
from main import *

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

import os


class UtilTest(unittest.TestCase):
    
    def test_dotenv_test(self):
        from dotenv import load_dotenv


        load_dotenv()

        pgadmin_dbname = os.getenv('PG_DBNAME')

        self.assertEqual('fastapiserverpostgresqldb', pgadmin_dbname)


class ClientTest(unittest.TestCase):
    client = TestClient(app)

    def test_read_root(self):
        response = self.client.get('/')
        
        self.assertEqual(200, response.status_code)
        self.assertEqual({"Hello":"World"}, response.json())


class DatabaseTest(unittest.TestCase):
    
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

    def test_read_root(self):
        response = self.client.get('/')
        
        self.assertEqual(200, response.status_code)
        self.assertEqual({"Hello":"World"}, response.json())

    def test_db(self):
        pass

if __name__ == '__main__':
    unittest.main()

