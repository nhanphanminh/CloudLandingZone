import os
from dotenv import load_dotenv
from pathlib import Path

ENV_FILE_DIR = "./.env"
dotenv_path = Path(ENV_FILE_DIR)
load_dotenv(dotenv_path=dotenv_path)

#get ENV
REGION = os.getenv("REGION")
print (REGION)