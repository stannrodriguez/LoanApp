from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class LoanForm(FlaskForm):
	name = TextAreaField('Loan Name', validators=[DataRequired()])
	balance = DecimalField('Current Balance', validators=[DataRequired()])
	int_rate = DecimalField('Interest Rate (APR)', validators=[DataRequired()])
	submit = SubmitField('Add Loan')

class IncomeForm(FlaskForm):
	income = DecimalField('Income (after taxes)', validators=[DataRequired()])
	income_pct = DecimalField('Percent to Commit for Loans', validators=[DataRequired()])
	submit = SubmitField('Submit')