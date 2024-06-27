import os
from dotenv import load_dotenv

env_name = os.getenv("ENV_NAME", "local")
env_file = f"config/.env.{env_name}"

load_dotenv(env_file)
