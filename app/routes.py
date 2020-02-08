from flask import render_template, redirect, url_for, flash, send_file
from app import app, db
from app.forms import LoanForm, IncomeForm
from app.models import loan_schedule
import plotly.express as px
import numpy as np
import pandas as pd

# from app.models import User, Loan
global user
user = {}
@app.route('/')
def index():
	return render_template('base.html', title='Pay It Off')

@app.route('/loans', methods=['GET', 'POST'])
def loans():
	# user = User()
	# db.session.add(user)
	# db.session.commit()

	form = LoanForm()
	if form.validate_on_submit():
		current_loan = 	{
				'name': form.name.data,
			 	'balance': form.balance.data,
			 	'int_rate': form.int_rate.data
			}
		try:
			loan_data.append(current_loan)
		except NameError:
			loan_data = [current_loan]
		user['loan_data'] = loan_data
		flash('Your loan data has been saved!')
		return render_template('loans.html', form=form, loans=loan_data)
	else:
		return render_template('loans.html', form=form)

@app.route('/income', methods=['GET', 'POST'])
def income(user):
	income_form = IncomeForm()
	income = [
		{
			'income': 60000,
			'income_pct': 20
		}
	]

	if income_form.validate_on_submit():
		income_data = {'income': income_form.income.data,
					   'income_pct': income_form.income_pct.data}
		user['income_data'] = income_data
		return redirect(url_for('strategy'))

	return render_template('income.html', form=income_form, income=income)

@app.route('/strategy', methods=['GET'])
def strategy():
	user = {
		'loan_data':[{
		'name': 'Chase',
		'balance': 50000,
		'int_rate': 8
		}
		]
	}
	schedule = loan_schedule(user['loan_data'][0])
	schedule.to_csv('app/DownloadFiles/LoanStrategy.csv')
	chart = px.area(schedule, x='Date', y='Remaining Balance', color='Name')

	return render_template('strategy.html',
							chart=chart.to_html(full_html=False), 
							data_preview=schedule.head().to_html(classes=['table']))

@app.route('/download')
def download():
	return send_file('DownloadFiles/LoanStrategy.csv',
		mimetype='text/csv', attachment_filename='LoanStrategy.csv',
		as_attachment=True)
