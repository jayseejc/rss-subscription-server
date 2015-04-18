from flask import Flask
from flask.ext.restful import Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from api_models import FeedApi, FeedListApi
from api import BASE_URI

api = Api(app)
api.add_resource(FeedApi, BASE_URI + '/feed/<int:id>', endpoint='feed')
api.add_resource(FeedListApi, BASE_URI +'/feeds', endpoint='feeds')

from app import models