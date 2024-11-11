from os import path, getenv
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY =  getenv("private_key").replace('\\n', '\n')
print(PRIVATE_KEY)