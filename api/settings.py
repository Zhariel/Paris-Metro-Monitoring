import os

from dotenv import load_dotenv
dotenv_path = os.path.join('..', '.env')
load_dotenv(dotenv_path)


#Credientials Used to get data
HEADERS = {
    'Authorization' : os.getenv('AUTH_TOKEN')
}
URL_BASE = os.getenv('URL')
LINES_ENDPOINT = os.getenv('LINES_ENDPOINT')
JOURNEYS_ENDPOINT = os.getenv('JOURNEYS_ENDPOINT')