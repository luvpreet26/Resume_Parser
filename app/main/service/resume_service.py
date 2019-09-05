import uuid
import datetime

from app.main import db
from sqlalchemy import and_
from werkzeug import secure_filename
from app.main.service import parsing_code
def parser_resume(file):
    filename = secure_filename(file.filename)
    file.save(filename)
    data = parsing_code.parsing(filename)
   # print(data)
    return data
