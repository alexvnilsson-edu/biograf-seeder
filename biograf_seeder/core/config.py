import os
import dotenv

try:
    dotenv_file = dotenv.find_dotenv(".env", usecwd=True)
except IOError:
    print("Kunde inte hitta .env-fil.")

dotenv.load_dotenv(dotenv_file)


def get(key: str):
    return os.getenv(key)
