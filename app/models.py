from app import db
from datetime import datetime
import numpy as np
import pandas as pd

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


def loan_schedule(loan, payment=1000, start_date=datetime.now()):
	"""
	Create amortization schedule for loan.
	loan: dict or DataFrame with the following keys or columns
		1) name 2) int_rate 3) balance
	payment: float or int, Default 1000
	start_date (optional): datetime object
	"""

	# Initialize variables and dataframe
	schedule = pd.DataFrame()
	num_payments = np.nper(loan['int_rate']/(100*12), -1000, loan['balance'])
	dates = pd.date_range(start=start_date,freq='M',periods=np.ceil(num_payments))
	int_rate, initial_balance = loan['int_rate']/100, loan['balance']

	# For each date, calculate interest and principal payment until balance is 0
	for date in dates:
		interest_payment = initial_balance*int_rate/12
		remaining_balance = initial_balance*(1+int_rate/12)-payment
		principal_payment = payment - interest_payment
		if payment > initial_balance + interest_payment:
		  principal_payment = initial_balance
		  remaining_balance = 0
		  payment = principal_payment + interest_payment
		schedule = schedule.append([
		    {
		        'Date': date,
		        'Initial Balance': initial_balance,
		        'Payment': payment,
		        'Interest Payment': interest_payment,
		        'Principal Payment': principal_payment,
		        'Remaining Balance': remaining_balance
		    }
		])
		initial_balance = remaining_balance
	# Insert Loan Information
	schedule.insert(1, 'Name', loan['name'])
	schedule.insert(2, 'Interest Rate', loan['int_rate'])
	# Clean Table
	schedule['Date'] = schedule['Date'].dt.strftime('%m/%d/%Y')
	schedule = schedule.set_index(['Date','Name']).round(2).reset_index()
	return schedule
