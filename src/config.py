from databases import Database
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config()
PROJECT_NAME = "Project Vodan API"
VERSION = "1.0.0"

MYSQL_HOSTNAME = config("MYSQL_HOSTNAME", cast=str, default="localhost")
MYSQL_DATABASE = config("MYSQL_DATABASE", cast=str, default="project_vodan")
MYSQL_USERNAME = config("MYSQL_USERNAME", cast=str, default="root")
MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=Secret)
MYSQL_PORT = config("MYSQL_PORT", cast=str, default="3306")


APP_PORT = config("APP_PORT", cast=int, default=8000)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}:{MYSQL_PORT}/{MYSQL_DATABASE}",
)

database = Database(DATABASE_URL, min_size=2, max_size=10)
