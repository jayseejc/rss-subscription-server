from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64),index=True,unique=True)
	password = db.Column(db.String(44),index=False,unique=False)
	feeds = db.relationship('Feed', backref='user', lazy='dynamic')

	def __repr__(self):
		return '<User %r>' % (self.name)

class Feed(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), index=True,unique=False)
	uri = db.Column(db.String(1024), index=True,unique=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))