#!/usr/bin/env python3

# All imports
from flask import Flask, render_template
from flask_restful import reqparse, Api, Resource
from manager import Manager

import json

# Settings
queue_name = 'queue_a_la_con'

# Manager

manager = Manager()

# Queue connection
connection = pika.BlockingConnection(pika.ConnectionParameters(
                                     'ec2-54-157-2-56.compute-1.amazonaws.com',
                                     5672))
channel = connection.channel()

channel.queue_declare(queue=queue_name)

# Application
app = Flask(__name__)
api = Api(app)

# Args parsing
parser = reqparse.RequestParser()

parser.add_argument('id', type=str, help='id of current client')
parser.add_argument('body', type=int, help='rate the task')

# API resources


class APIResgistration(Resource):

    def get(self):
        return {'status': 'OK'}, 200

    def post(self):
        args = parser.parse_args()
        if args.id = manager.addNode(args.id):
            if manager.getRemainingCollabs() == 0:
                manager.sendGoSignal()
            return manager.getConfig(), 201
        else:
            return 'exceeded quota', 403

# Routes binding
api.add_resource(APIResgistration, '/registration')

# main
if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: %s config-file.json [result-file]' % sys.argv[0])

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: config file %s was not found' % sys.argv[1])

    manager.readConfig(sys.argv[1])

    print("SERVER is starting")
    app.run(debug=False)
