from flask import Flask, send_from_directory
# from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from flask import Flask

app = Flask(__name__)
CORS(app)


@app.route('/stations')
def serve():
    return "aaaaa"

if __name__ == '__main__':
    app.run()
