from flask.ext.restful import Resource, reqparse, marshal, fields
from flask.ext.httpauth import HTTPBasicAuth
from flask import request
from app import models, db, api
from models import User, Feed

auth = HTTPBasicAuth()

feed_fields = {
	'title': fields.String,
	'uri': fields.String,
	'url': fields.Url('feed'),
	'id': fields.String
}

class FeedApi(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str, location = 'json')
		self.reqparse.add_argument('description', type = str, location = 'json')
		self.reqparse.add_argument('done', type = bool, location = 'json')
		super(FeedApi, self).__init__()

	def post(self,id):
		if(authenticate_user(request.form['username'], request.form['password'])):
			user=models.User.query.filter_by(name=request.form['username']).first()
			# id = int(request.form['id'])
			for feed in user.feeds:
				if feed.id == id:
					return {'feed': marshal(feed,feed_fields)}
			return {'error':'Feed not found'}, 404
		else:
			return {'error':'Invallid authentication'}, 401

	def delete(self, id):
		if(authenticate_user(request.form['username'], request.form['password'])):
			user=models.User.query.filter_by(name=request.form['username']).first()
			for feed in user.feeds:
				if feed.id == id:
					db.session.delete(feed)
			db.session.commit()
		else:
			return {'error':'Invallid authentication'}, 401

class FeedListApi(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str, required = True,
            help = 'No task title provided', location = 'json')
		self.reqparse.add_argument('description', type = str, default = "", location = 'json')
		super(FeedListApi, self).__init__()

	def post(self):
		if(authenticate_user(request.form['username'], request.form['password'])):
			feeds = models.User.query.filter_by(name=request.form['username']).first().feeds.all()
			return { "feeds": [marshal(feed, feed_fields) for feed in feeds]}
		else:
			return {'error':'Invallid authentication'}, 401

def create_user(username, password):
	return api.create_user(username,password)

def authenticate_user(username, password):
	return api.authenticate_user(username, password)