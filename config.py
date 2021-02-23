from flask_sqlalchemy import SQLAlchemy
DATABASE_NAME = "measurements"
END_POINT = "localhost:5432"
USERNAME = "rootuser"
PASSWORD = "rootuser"
AUTH0_DOMAIN = ""
ALGORITHMS = ['RS256']
API_AUDIENCE = 'devices'
DATABASE_PATH = "postgres://{}:{}@{}/{}".format(
                                                USERNAME, 
                                                PASSWORD, 
                                                END_POINT, 
                                                DATABASE_NAME
                                                )
db = SQLAlchemy()
