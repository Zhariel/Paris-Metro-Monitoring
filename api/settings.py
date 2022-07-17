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
RDS_USER = os.getenv('RDS_USER')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_DATABASE = os.getenv('RDS_DATABASE')
RDS_URL = os.getenv('RDS_URL')
RDS_PORT = os.getenv('RDS_PORT')