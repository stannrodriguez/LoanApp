from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filler = db.Column(db.String)
	loans = db.relationship('Loan', backref='user', lazy='dynamic')
	income = db.relationship('Income', backref='user', lazy='dynamic')

	def __repr__(self):
		return f'<User Id: {self.filler, self.id}>'

class Loan(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	balance = db.Column(db.Float)
	int_rate = db.Column(db.Float)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Income(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	income = db.Column(db.Float)
	income_pct = db.Column(db.Float)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
