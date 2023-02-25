import os
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:5432/{os.environ["DB_NAME"]}'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
