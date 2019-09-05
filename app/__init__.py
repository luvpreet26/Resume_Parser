# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.job_position_controller import api as user_ns

#from .main.controller.job_position_controller import apix as application_ns

blueprint = Blueprint('api', __name__,url_prefix='/parsing')

api = Api(blueprint,
          title='Resume Pasring Service',
          version='1.0',
          description='A resume parsing service',
        
          )

api.add_namespace(user_ns)
