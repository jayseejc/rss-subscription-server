from app import app, db, models
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify

BASE_URI='/rss-provider/api/v1.0'

@app.route(BASE_URI + "/feed/new", methods=['POST'])
def new_feed():
	if authenticate_user(request.form['username'], request.form['password']):
		user=models.User.query.filter_by(name=request.form['username']).first()
		title=request.form['title']
		uri=request.form['uri']
		for feed in user.feeds:
			if feed.title == title:
				return jsonify({'error': 'Another feed by the same name already exists.'}), 409
		create_feed(user, title, uri)
		feed=models.Feed.query.filter_by(title=title).first()
		return jsonify({'id':feed.id})
	else:
		return jsonify({'error':'Invallid authentication'}), 401

@app.route(BASE_URI+"/user/new", methods=['POST'])
def new_user():
	username=request.form['username']
	u = models.User.query.filter_by(name=username).first()
	if u is not None:
		return jsonify({'error':'User exists'}), 409
	create_user(username, request.form['password'])
	u=models.User.query.filter_by(name=username).first()
	return jsonify({'id':u.id})

def authenticate_user(username, password):
	u = models.User.query.filter_by(name=username).first()
	if u is None:
		return False
	if check_password_hash(u.password, password):
		return True
	return False

def create_user(username, password):
	password=generate_password_hash(password)
	u=models.User(name=username,password=password);
	db.session.add(u)
	db.session.commit()

def create_feed(user, title, url):
	f = models.Feed(user=user,title=title,uri=url)
	db.session.add(f)
	db.session.commit()