import os

from dotenv import load_dotenv

load_dotenv()

class InfluxDBConfig: 
    USERNAME = os.environ.get("INFLUX_USERNAME") or "just_for_dev"
    PASSWORD = os.environ.get("INFLUX_PASSWORD") or "password_for_dev"
    HOST = os.environ.get("INFLUX_HOST") or "localhost"
    PORT = os.environ.get("INFLUX_PORT") or "27017"
    DATABASE = os.environ.get("INFLUX_DATABASE") or "example_db"