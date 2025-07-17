import os
from dotenv import load_dotenv
load_dotenv()

def get_connection_string():
    return "postgresql://{user}:{password}@{host}:{port}/{db}".format(
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", "root"),
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", 5432),
        db=os.environ.get("POSTGRES_DB", "hr_management"),
    )