import os

from dotenv import load_dotenv

load_dotenv('envs/.env')

print(os.getenv('SECRET_KEY'))