#!/usr/bin/env python3
from flask import Flask
from flask_restful import reqparse, Api, Resource
from controller import Controller
import logging
import getopt
import sys
import os


# Manager
controller = Controller()

# Application
app = Flask(__name__)
api = Api(app)

# Args parsing
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, help='id of current client')

complex_parser = reqparse.RequestParser()
complex_parser.add_argument('id', type=str, help='id of current client')
complex_parser.add_argument('payload', type=str, help='results of experience')

logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# API resources

class APIResgistration(Resource):

    def get(self):
        return {'status': 'Bad Method'}, 400

    def post(self):
        args = parser.parse_args()
        return {'status': 'OK', 'body': controller.addNode(args.id)}, 201


class APIAcknowledgement(Resource):

    def get(self):
        return {'status': 'Bad Method'}, 400

    def post(self):
        args = parser.parse_args()
        controller.acknowledgeRegistration(args.id)
        return {'status': 'OK'}, 201


class APISaveResults(Resource):

    def get(self):
        return {'status': 'Bad Method'}, 400

    def post(self):
        args = complex_parser.parse_args()
        controller.saveResults(args.id, args.payload)
        return {'status': 'OK'}, 201


class APIForceExp(Resource):

    def get(self):
        controller.startExp()
        return {'satus': 'SERVER_IS_RUNNING',
                'details': 'Start signal will be send'
                }, 201

    def post(self):
        return {'status': 'Bad Method'}, 400


class APIStatus(Resource):

    def get(self):
        return {'satus': 'SERVER_IS_RUNNING',
                'details': controller.getStatus(),
                }, 201

    def post(self):
        return {'status': 'Bad Method'}, 400


# Routes binding

api.add_resource(APIResgistration, '/registration')
api.add_resource(APIAcknowledgement, '/acknowledgement')
api.add_resource(APISaveResults, '/saveresults')
api.add_resource(APIForceExp, '/forceexp')
api.add_resource(APIStatus, '/status')

# Main

if __name__ == '__main__':

    logger.debug("=== SERVER is starting ===")

    env_var = False
    path_file = ""

    if len(sys.argv) < 2:
        sys.exit('Usage: %s -e | -f config-file.json' % sys.argv[0])

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ef:")
    except getopt.GetoptError:
        sys.exit('Usage: %s -e | -f config-file.json' % sys.argv[0])

    for opt, arg in opts:
        if opt == '-e':
            logger.debug("=== Environment varibles will be used ===")
            env_var = True
            break
        elif opt == '-f':
            logger.debug("=== Configuration file will be used ===")
            path_file = arg
            if not os.path.exists(path_file):
                sys.exit('ERROR: config file %s was not found' % path_file)

    logger.debug("=== Config is being read ===")

    if not controller.readConfig(env_var, path_file):
        sys.exit('ERROR: cofig file is not well formed')

    ip_address = os.getenv('SERVER_ADDRESS', '127.0.0.1')
    logger.debug('SERVER_ADDRESS %s' % ip_address)
    app.run(host=ip_address, debug=True)
