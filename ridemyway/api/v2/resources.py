"""
    v2 API resources
    Resources check for presence of required data and pass to errors
    for semantic error checks
    Clean data without semantic errors is further handled by the controllers
"""

import json

from flask_restful import Resource, reqparse

from .controllers.auth import AuthController
from ridemyway.utils import errors


auth = AuthController()


class Signup(Resource):
    """
        SIGNUP Resource
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username',
                                 help='This field cannot be blank',
                                 required=True)
        self.parser.add_argument('name',
                                 help='This field cannot be blank',
                                 required=True)
        self.parser.add_argument('gender',
                                 help='This field cannot be blank',
                                 required=True)
        self.parser.add_argument('usertype',
                                 help='This field cannot be blank',
                                 required=True)
        self.parser.add_argument('email',
                                 help='This field cannot be blank',
                                 required=True)
        self.parser.add_argument('password',
                                 help='This field cannot be blank',
                                 required=True)
        self.parser.add_argument('contacts',
                                 help='This field cannot be blank',
                                 required=True)

    def post(self):
        """
            User SIGNUP
        """
        data = self.parser.parse_args()
        signup_errors = errors.signup_errors(**data)
        if signup_errors:
            return json.loads(json.dumps(signup_errors)), 422
        return auth.signup(**data)