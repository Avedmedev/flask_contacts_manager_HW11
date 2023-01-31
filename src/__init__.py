from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

app = Flask(__name__)
app.debug = True

app.config.from_object(config.Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

session = db.session

from src import routes, models
