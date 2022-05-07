import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

GEODISTANCE_USERNAME = os.getenv('GEODISTANCE_USERNAME')
GEODISTANCE_PASSWORD = os.getenv('GEODISTANCE_PASSWORD')
