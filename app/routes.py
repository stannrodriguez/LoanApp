from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import LoanForm, IncomeForm
# from app.models import User, Loan

@app.route('/')
def index():
	return render_template('base.html', title='Pay It Off')

@app.route('/loans', methods=['GET', 'POST'])
def loans():
	# user = User()
	# db.session.add(user)
	# db.session.commit()
	loans = []
	form = LoanForm()
	if form.validate_on_submit():
		# loan = Loan(name=form.name.data, balance=form.balance.data,
		# 			int_rate=form.int_rate.data, user=user)
		flash('Your loan data has been saved!')
		# loans = user.loans.all()
		loans = [
			{
				'name': 'Chase',
				'balance': 27808.80,
				'int_rate': 8.615
			},
			{
				'name': 'Sallie Mae',
				'balance': 54186.21,
				'int_rate': 10.125
			}
		]
		return render_template('loans.html', form=form, loans=loans)

	return render_template('loans.html', form=form, loans=loans)

@app.route('/income', methods=['GET', 'POST'])
def income():
	income_form = IncomeForm()
	income = [
		{
			'income': 60000,
			'income_pct': 20}
	]

	if income_form.validate_on_submit():
		return render_template('strategy.html')

	return render_template('income.html', form=income_form, income=income)

@app.route('/strategy')
def strategy():
	return render_template('strategy.html')
