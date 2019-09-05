from flask import request
from flask_restplus import Resource

from ..util.dto import resume
api = resume.api

_resume = resume.parser_template
from ..service.resume_service import parser_resume

@api.route('/')
class UserList(Resource):
    @api.expect(_resume, validate=True)
    def post(self):
        """Creates a new job position """
        file = request.files['resume_file']
        return parser_resume(file)

