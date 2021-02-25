import os
DATABASE_NAME = "measurements"
END_POINT = "localhost:5432"
USERNAME = "rootuser"
PASSWORD = "rootuser"
AUTH0_DOMAIN = os.environ.get('auth_domain')
ALGORITHMS = eval(os.environ.get('algorithms'))
API_AUDIENCE = os.environ.get('api_audiance')
DATABASE_PATH = os.environ.get("database_path")
