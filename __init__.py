#!/usr/bin/env python3

# All imports
from flask import Flask, render_template
from flask_restful import reqparse, Api, Resource
from manager import Manager
import sys
import os
import json


# Manager

manager = Manager()

# Application
app = Flask(__name__)
api = Api(app)

# Args parsing
parser = reqparse.RequestParser()

parser.add_argument('id', type=str, help='id of current client')

# API resources


class APIResgistration(Resource):

    def get(self):
        return {'status': 'Bad Method'}, 400

    def post(self):
        args = parser.parse_args()
        if manager.addNode(args.id):
            return manager.getConfig(), 201
        else:
            return {'status': 'exceeded quota or node already registrated'}, 403


class APIAcknowledgement(Resource):

    def get(self):
        return {'status': 'Bad Method'}, 400

    def post(self):
        args = parser.parse_args()
        manager.acknowledgeRegistration(args.id)
        return {'status': 'OK'}, 201


# Routes binding

api.add_resource(APIResgistration, '/registration')
api.add_resource(APIAcknowledgement, '/acknowledgement')

# Main

if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: %s config-file.json [result-file]' % sys.argv[0])

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: config file %s was not found' % sys.argv[1])

    if not manager.readConfig(sys.argv[1]):
        sys.exit('ERROR: cofig file is not well formed')

    print("SERVER is starting")
    app.run(debug=False)
