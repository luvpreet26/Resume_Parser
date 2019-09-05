from flask_restplus import Namespace, fields
import werkzeug

class resume:
    api = Namespace('resume', description='job_position')
    parser_template = api.parser()
    parser_template.add_argument('resume_file', required = True, type=werkzeug.datastructures.FileStorage, location='files')
    