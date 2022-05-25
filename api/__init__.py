import os

from dotenv import load_dotenv
dotenv_path = os.path.join('..', '.env')
load_dotenv(dotenv_path)


#Credientials Used to get data
HEADERS = {
    'Authorization' : os.getenv('AUTH_TOKEN')
}
URL = os.getenv('URL')