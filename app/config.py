from pydantic_settings import BaseSettings 
from dotenv import load_dotenv 
import os # to access the env variables

load_dotenv() # initializing load env

class Settings(BaseSettings):
    mongo_url : str = os.environ.get("MONGODB_URL")
    db_name : str = os.environ.get("DB_NAME")
    collection_name : str =  os.environ.get("MONGODB_URL")

    class config:
        env_file = '.env'

settings = Settings()