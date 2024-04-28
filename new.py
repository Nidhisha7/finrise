import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Retrieve financial information
cur.execute('''SELECT * FROM UserFinancialInfo''')
financial_info = cur.fetchone()  # Assuming there's only one financial record per user
# Retrieve expenses data
cur.execute('''INSERT INTO Expenses(income,housing,utilities,daily_transportation,food,debt_payments,healthcare,insurance,taxes, housing_importance,utilities_importance,daily_transportation_importance,food_importance,debt_payments_importance,healthcare_importance,insurance_importance,taxes_importance,savings,education,charity,savings_importance,education_importance,charity_importance,entertainment,personal_care,miscellaneous,vacation,entertainment_importance,personal_care_importance,miscellaneous_importance,vacation_importance) VALUES (10000,10000,1500,200,500,0,0,300,5000,3,2,1,2,1,1,1,1,10000,3000,200,3,1,2,10000,5000,1000,0,1,2,1,1)''')
conn.commit()

cur.execute('''SELECT income FROM Expenses''')
income=cur.fetchone()
for item in income:
    income=item

#for essential category
cur.execute('''SELECT housing,utilities,daily_transportation,food,debt_payments,healthcare,insurance,taxes FROM Expenses''')
essential_data = cur.fetchone()
cur.execute('''SELECT housing_importance,utilities_importance,daily_transportation_importance,food_importance,debt_payments_importance,healthcare_importance,insurance_importance,taxes_importance FROM Expenses''')
essential_imp = cur.fetchone()


#for savings category
cur.execute('''SELECT  savings,education,charity FROM Expenses''')
savings_data = cur.fetchone()
cur.execute('''SELECT savings_importance,education_importance,charity_importance FROM Expenses''')
savings_imp = cur.fetchone()  

#for personal category
cur.execute('''SELECT  entertainment,personal_care,miscellaneous, vacation FROM Expenses''')
personal_data = cur.fetchone()
cur.execute('''SELECT entertainment_importance,personal_care_importance,miscellaneous_importance,vacation_importance FROM Expenses''')
personal_imp = cur.fetchone()  

#set limits
essential_limit=0.6*income
savings_limit=0.2*income
personal_limit=0.2*income

if(sum(essential_data)>sum(savings_data) and sum(essential_data)>sum(personal_data)):
    if(sum(essential_data)>essential_limit):
        essential_imp_filtered = [imp for imp, expense in zip(essential_imp, essential_data) if expense != 0]
        print(essential_imp_filtered)
        essential_data_filtered = [expense for expense in essential_data if expense != 0]
        print(essential_data_filtered)
        essential_category = [expense for imp, expense in zip(essential_imp_filtered, essential_data_filtered) if imp == min(essential_imp_filtered)]
        max_index = essential_data.index(max(essential_category))
        essential = ['housing', 'utilities', 'daily_transportation', 'food', 'debt_payments', 'healthcare', 'insurance', 'taxes']
        print("Attribute corresponding to the maximum value in essential_category:", essential[max_index])

elif (sum(savings_data)>sum(essential_data) and sum(savings_data)>sum(personal_data)):
    if(sum(savings_data) > savings_limit):
        savings_imp_filtered = [imp for imp, expense in zip(savings_imp, savings_data) if expense != 0]
        savings_data_filtered = [expense for expense in savings_data if expense != 0]
        savings_category = [expense for imp, expense in zip(savings_imp_filtered, savings_data_filtered) if imp == min(savings_imp_filtered)]
        max_index = savings_data.index(max(savings_category))
        # Retrieve the corresponding attribute using the index
        savings_attributes = ['savings', 'education', 'charity']
        print("Attribute corresponding to the maximum value in savings_category:", savings_attributes[max_index])

elif (sum(personal_data)>sum(essential_data) and sum(savings_data)<sum(personal_data)):
    if(sum(personal_data) > personal_limit):
        personal_imp_filtered = [imp for imp, expense in zip(personal_imp, personal_data) if expense != 0]
        personal_data_filtered = [expense for expense in personal_data if expense != 0]
        personal_category = [expense for imp, expense in zip(personal_imp_filtered, personal_data_filtered) if imp == min(personal_imp_filtered)]
        max_index = personal_data.index(max(personal_category))
        # Retrieve the corresponding attribute using the index
        personal_attributes =['entertainment', 'personal_care', 'miscellaneous', 'vacation']
        print("Attribute corresponding to the maximum value in personal_category:", personal_attributes[max_index])


"""
            @app.route('/report/<int:year>/<string:month>')
def generate_report(year, month):
    # Retrieve data from the database based on the provided month, year, and user email
    if 'email' in session:
        user_email = session['email']
        conn = connect_db()
        cur = conn.cursor()
        try:
            # Retrieve financial information
            cur.execute('''SELECT email, financial_goal, time_period FROM UserFinancialInfo WHERE email=?''', (user_email,))
            financial_info = cur.fetchone()
            financial_goal = financial_info[1]
            time_period = financial_info[2]

            # Retrieve expenses data
            cur.execute('''SELECT email, income, month, year,
                                vacation, daily_transportation, utilities, savings, housing, 
                                debt_payments, healthcare, personal_care, food, insurance, 
                                education, entertainment, charity, taxes, miscellaneous, 
                                vacation_importance, daily_transportation_importance, utilities_importance, 
                                savings_importance, housing_importance, debt_payments_importance, 
                                healthcare_importance, personal_care_importance, food_importance, 
                                insurance_importance, education_importance, entertainment_importance, 
                                taxes_importance, charity_importance, miscellaneous_importance
                           FROM Expenses 
                           WHERE email=? AND month=? AND year=?''', (user_email, month, year))
            expenses_data = cur.fetchall()

            cur.execute('''SELECT income FROM Expenses''')
            income = cur.fetchone()[0]

            # for essential category
            cur.execute('''SELECT housing, utilities, daily_transportation, food, debt_payments, healthcare, insurance, taxes FROM Expenses''')
            essential_data = cur.fetchone()
            cur.execute('''SELECT housing_importance, utilities_importance, daily_transportation_importance, food_importance, debt_payments_importance, healthcare_importance, insurance_importance, taxes_importance FROM Expenses''')
            essential_imp = cur.fetchone()

            # for savings category
            cur.execute('''SELECT savings, education, charity FROM Expenses''')
            savings_data = cur.fetchone()
            cur.execute('''SELECT savings_importance, education_importance, charity_importance FROM Expenses''')
            savings_imp = cur.fetchone()

            # for personal category
            cur.execute('''SELECT entertainment, personal_care, miscellaneous, vacation FROM Expenses''')
            personal_data = cur.fetchone()
            cur.execute('''SELECT entertainment_importance, personal_care_importance, miscellaneous_importance, vacation_importance FROM Expenses''')
            personal_imp = cur.fetchone()  

            # Set limits
            essential_limit = 0.6 * income
            savings_limit = 0.2 * income
            personal_limit = 0.2 * income

            # Determine the category with the highest spending and select the attribute
            if sum(essential_data) > sum(savings_data) and sum(essential_data) > sum(personal_data):
                if sum(essential_data) > essential_limit:
                    essential_imp_filtered = [imp for imp, expense in zip(essential_imp, essential_data) if expense != 0]
                    essential_data_filtered = [expense for expense in essential_data if expense != 0]
                    essential_category = [expense for imp, expense in zip(essential_imp_filtered, essential_data_filtered) if imp == min(essential_imp_filtered)]
                    max_index = essential_data.index(max(essential_category))
                    essential = ['housing', 'utilities', 'daily_transportation', 'food', 'debt_payments', 'healthcare', 'insurance', 'taxes']
                    max_category = essential[max_index]

            elif sum(savings_data) > sum(essential_data) and sum(savings_data) > sum(personal_data):
                if sum(savings_data) > savings_limit:
                    savings_imp_filtered = [imp for imp, expense in zip(savings_imp, savings_data) if expense != 0]
                    savings_data_filtered = [expense for expense in savings_data if expense != 0]
                    savings_category = [expense for imp, expense in zip(savings_imp_filtered, savings_data_filtered) if imp == min(savings_imp_filtered)]
                    max_index = savings_data.index(max(savings_category))
                    savings_attributes = ['savings', 'education', 'charity']
                    max_category = savings_attributes[max_index]

            elif sum(personal_data) > sum(essential_data) and sum(savings_data) < sum(personal_data):
                if sum(personal_data) > personal_limit:
                    personal_imp_filtered = [imp for imp, expense in zip(personal_imp, personal_data) if expense != 0]
                    personal_data_filtered = [expense for expense in personal_data if expense != 0]
                    personal_category = [expense for imp, expense in zip(personal_imp_filtered, personal_data_filtered) if imp == min(personal_imp_filtered)]
                    max_index = personal_data.index(max(personal_category))
                    personal_attributes = ['entertainment', 'personal_care', 'miscellaneous', 'vacation']
                    max_category = personal_attributes[max_index]
"""
"""
            # Fetch the sum of savings from the Expenses table
            cur.execute("""SELECT SUM(savings) FROM Expenses WHERE email=?""", (user_email,))
            sav = cur.fetchone()
            total_savings = sav[0] if sav else 0.0  # Use 0.0 if no savings are found
            remaining = financial_goal - total_savings

            return render_template('report.html', month=month, year=year, financial_info=financial_info, expenses_data=expenses_data, max_category=max_category, remaining=remaining)

        except Exception as e:
            # Log the exception and traceback
            traceback.print_exc()
            return jsonify({'error': 'An error occurred while retrieving the report data. Please try again later.'})
        finally:
            # Close the cursor and database connection
            cur.close()
            conn.close()

    else:
        return jsonify({'error': 'Unauthorized access. Please log in.'})
"""
@app.route('/input', methods=['POST', 'GET'])
def input():
    if 'email' in session:
        if request.method == 'POST':
            conn = connect_db()
            cur = conn.cursor()
                
            try:
                
                # Get the form data from the request
                income = float(request.form.get('income', 0))
                month = request.form.get('month', '')
                year = int(request.form.get('year', 0))
                time_period = int(request.form.get('timePeriod', 0))  # Corrected field name
                financial_goal = float(request.form.get('financialGoal', 0))  # Corrected field name

            # Insert financial info into UserFinancialInfo table
                cur.execute("""INSERT INTO UserFinancialInfo(email, time_period, financial_goal) VALUES (?, ?, ?)""", 
            (session['email'], time_period, financial_goal))

                # Extract expenses and importances from the form data
                expenses = {key: float(request.form[key]) if request.form[key] != '' else 0.0 for key in request.form if key not in ['income', 'month', 'year', 'timePeriod', 'financialGoal']}
                importances = {key.replace('-importance', ''): int(request.form.get(key, 0)) for key in request.form if key.endswith('-importance')}

                # Create a tuple containing all the values for the INSERT statement
                t = (session['email'], income, month, year) + tuple(expenses.get(key, 0) for key in ['Vacation', 'daily-transportation', 'utilities', 'savings',
                                                    'housing', 'debt-payments', 'healthcare', 'personal-care',
                                                    'food', 'insurance', 'education', 'entertainment',
                                                    'charity', 'taxes', 'miscellaneous']) + tuple(importances.get(key, 0) for key in ['Vacation', 'daily-transportation', 'utilities', 'savings',
                                                       'housing', 'debt-payments', 'healthcare', 'personal-care',
                                                       'food', 'insurance', 'education', 'entertainment',
                                                       'charity', 'taxes', 'miscellaneous'])

# Insert financial data into the Expenses table
                cur.execute('''INSERT INTO Expenses 
               (email, income, month, year,
                vacation, daily_transportation, utilities, savings, housing, 
                debt_payments, healthcare, personal_care, food, insurance, 
                education, entertainment, charity, taxes, miscellaneous,
                vacation_importance, daily_transportation_importance, utilities_importance, 
                savings_importance, housing_importance, debt_payments_importance, 
                healthcare_importance, personal_care_importance, food_importance, 
                insurance_importance, education_importance, entertainment_importance, 
                charity_importance, taxes_importance, miscellaneous_importance) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', t)
                conn.commit()
                return redirect(url_for('generate_report', month=month, year=year))
            except Exception as e:
                traceback.print_exc()
                conn.rollback()
                return jsonify({'error': 'An error occurred while processing your request. Please try again later.'}), 500
            finally:
                cur.close()
                conn.close()
        else:
            return render_template('input.html')
    else:
        return jsonify({'error': 'Unauthorized access. Please log in.'}) 

""""

@app.route('/update/<int:year>/<string:month>', methods=['POST','GET'])
"""
@app.route('/update/<int:year>/<string:month>', methods=['GET', 'POST'])
def update_expense(year, month):
	if 'email' in session:
		user_email = session['email']
		if request.method == 'POST':
			conn = connect_db()
			cur = conn.cursor()
			try:
				expenses = {key.lower(): float(request.form[key]) if request.form[key] != '' else 0.0 for key in request.form if key.lower() not in ['income', 'month', 'year', 'timeperiod', 'financialgoal']}
				importances = {key.lower().replace('-importance', ''): int(request.form.get(key, 0)) for key in request.form if key.endswith('-importance')}
				cur.execute("""SELECT vacation, daily_transportation, utilities, savings, housing, 
			debt_payments, healthcare, personal_care, food, insurance, 
			education, entertainment, charity, taxes, miscellaneous, income,
			vacation_importance, daily_transportation_importance, utilities_importance, savings_importance,
			housing_importance, debt_payments_importance, healthcare_importance, personal_care_importance,
			food_importance, insurance_importance, education_importance, entertainment_importance,
			charity_importance, taxes_importance, miscellaneous_importance
			FROM Expenses 
			WHERE email=? AND month=? AND year=?""",
			(user_email, month, year))
				existing_data = cur.fetchone()
		
		# Check if form values are different from existing values
				if existing_data != (tuple(expenses.get(key, 0) for key in ['vacation', 'daily_transportation', 'utilities', 'savings',
																  'housing', 'debt_payments', 'healthcare', 'personal_care',
																  'food', 'insurance', 'education', 'entertainment',
																  'charity', 'taxes', 'miscellaneous', 'income']) +
							 tuple(importances.get(key, 0) for key in ['vacation', 'daily_transportation', 'utilities', 'savings',
																		'housing', 'debt_payments', 'healthcare', 'personal_care',
																		'food', 'insurance', 'education', 'entertainment',
																		'charity', 'taxes', 'miscellaneous']) +
							 (user_email, month, year)):
			# Update the expense data and importances in the database
					cur.execute("""UPDATE Expenses 
					SET vacation=?, daily_transportation=?, utilities=?, savings=?, housing=?, 
						debt_payments=?, healthcare=?, personal_care=?, food=?, insurance=?, 
						education=?, entertainment=?, charity=?, taxes=?, miscellaneous=?, income=?,
						vacation_importance=?, daily_transportation_importance=?, utilities_importance=?, savings_importance=?,
						housing_importance=?, debt_payments_importance=?, healthcare_importance=?, personal_care_importance=?,
						food_importance=?, insurance_importance=?, education_importance=?, entertainment_importance=?,
						charity_importance=?, taxes_importance=?, miscellaneous_importance=?
					WHERE email=? AND month=? AND year=?""",
				tuple(expenses.get(key, 0) for key in ['vacation', 'daily_transportation', 'utilities', 'savings',
														'housing', 'debt_payments', 'healthcare', 'personal_care',
														'food', 'insurance', 'education', 'entertainment',
														'charity', 'taxes', 'miscellaneous', 'income']) +
				tuple(importances.get(key, 0) for key in ['vacation', 'daily_transportation', 'utilities', 'savings',
														   'housing', 'debt_payments', 'healthcare', 'personal_care',
														   'food', 'insurance', 'education', 'entertainment',
														   'charity', 'taxes', 'miscellaneous']) +
				(user_email, month, year))
				conn.commit()
				return render_template('report.html', month=month, year=year)
			except Exception as e:
			# Log the exception and traceback
				traceback.print_exc()
				return jsonify({'error': 'An error occurred while retrieving the report data. Please try again later.'})
			finally:
			# Close the cursor and database connection
				cur.close()
				conn.close()
		else:
			conn = connect_db()
			cur = conn.cursor()
			try:
				cur.execute("""SELECT vacation, daily_transportation, utilities, savings, housing, 
					debt_payments, healthcare, personal_care, food, insurance, 
					education, entertainment, charity, taxes, miscellaneous,income,
					vacation_importance, daily_transportation_importance, utilities_importance, 
					savings_importance, housing_importance, debt_payments_importance, 
					healthcare_importance, personal_care_importance, food_importance, 
					insurance_importance, education_importance, entertainment_importance, 
					charity_importance, taxes_importance, miscellaneous_importance
					FROM Expenses 
					WHERE email=? AND month=? AND year=?""",
					(user_email, month, year))
				expenses = cur.fetchone()
				if expenses:
			# If financial info exists, extract values
					vacation = expenses[0]
					daily_transportation = expenses[1]
					utilities = expenses[2]
					savings = expenses[3]
					housing = expenses[4]
					debt_payments = expenses[5]
					healthcare = expenses[6]
					personal_care = expenses[7]
					food = expenses[8]
					insurance = expenses[9]
					education = expenses[10]
					entertainment = expenses[11]
					charity = expenses[12]
					taxes = expenses[13]
					miscellaneous = expenses[14]
					income = expenses[15]
					vacation_importance = expenses[16]
					daily_transportation_importance = expenses[17]
					utilities_importance = expenses[18]
					savings_importance = expenses[19]
					housing_importance = expenses[20]
					debt_payments_importance = expenses[21]
					healthcare_importance = expenses[22]
					personal_care_importance = expenses[23]
					food_importance = expenses[24]
					insurance_importance = expenses[25]
					education_importance = expenses[26]
					entertainment_importance = expenses[27]
					charity_importance = expenses[28]
					taxes_importance = expenses[29]
					miscellaneous_importance = expenses[30]
				else:
				# If no financial info exists, set default values
					vacation = 0
					daily_transportation = 0
					utilities = 0
					savings = 0
					housing = 0
					debt_payments = 0
					healthcare = 0
					personal_care = 0
					food = 0
					insurance = 0
					education = 0
					entertainment = 0
					charity = 0
					taxes = 0
					miscellaneous = 0
					income = 0
					vacation_importance = 0
					daily_transportation_importance = 0
					utilities_importance = 0
					savings_importance = 0
					housing_importance = 0
					debt_payments_importance = 0
					healthcare_importance = 0
					personal_care_importance = 0
					food_importance = 0
					insurance_importance = 0
					education_importance = 0
					entertainment_importance = 0
					charity_importance = 0
					taxes_importance = 0
					miscellaneous_importance = 0
				return render_template('update.html', year=year, month=month, vacation=vacation,
                               daily_transportation=daily_transportation, utilities=utilities,
                               savings=savings, housing=housing, debt_payments=debt_payments,
                               healthcare=healthcare, personal_care=personal_care, food=food,
                               insurance=insurance, education=education, entertainment=entertainment,
                               charity=charity, taxes=taxes, miscellaneous=miscellaneous,
                               vacation_importance=vacation_importance,
                               daily_transportation_importance=daily_transportation_importance,
                               utilities_importance=utilities_importance,
                               savings_importance=savings_importance, housing_importance=housing_importance,
                               debt_payments_importance=debt_payments_importance,
                               healthcare_importance=healthcare_importance,
                               personal_care_importance=personal_care_importance,
                               food_importance=food_importance, insurance_importance=insurance_importance,
                               education_importance=education_importance,
                               entertainment_importance=entertainment_importance,
                               charity_importance=charity_importance, taxes_importance=taxes_importance,
                               miscellaneous_importance=miscellaneous_importance,
                               income=income)
				return render_template('report.html', month=month, year=year)
			except Exception as e:
				traceback.print_exc()
				return jsonify({'error': 'An error occurred while processing your request. Please try again later.'}), 500
			finally:
				cur.close()
				conn.close()
			
	else:
		return jsonify({'error': 'Unauthorized access. Please log in.'})
"""

income = float(request.form.get('income', 0) or 0)
				month = str(request.form.get('month',"null"))
				year = request.form.get('year',"null")
                                
                                else:
			conn = connect_db()
			cur = conn.cursor()
			try:
				income = float(request.form.get('income', 0) or 0)
				month = str(request.form.get('month',"null"))
				year = request.form.get('year',"null")
				cur.execute("SELECT time_period, financial_goal FROM UserFinancialInfo WHERE email=?", (session['email'],))
				financial_info = cur.fetchone()
				print(year," ",month)
				if financial_info:
					# If financial info exists, extract values
					time_period = financial_info[0]
					financial_goal = financial_info[1]
				else:
					# If no financial info exists, set default values
					time_period = 0
					financial_goal = 0
				cur.execute("""SELECT vacation, daily_transportation, utilities, savings, housing, 
					debt_payments, healthcare, personal_care, food, insurance, 
					education, entertainment, charity, taxes, miscellaneous,income,
					vacation_importance, daily_transportation_importance, utilities_importance, 
					savings_importance, housing_importance, debt_payments_importance, 
					healthcare_importance, personal_care_importance, food_importance, 
					insurance_importance, education_importance, entertainment_importance, 
					charity_importance, taxes_importance, miscellaneous_importance
					FROM Expenses 
					WHERE email=? AND month=? AND year=?""",
					(user_email, month, year))
				expenses = cur.fetchone()
				if expenses:
			# If financial info exists, extract values
					vacation = expenses[0]
					daily_transportation = expenses[1]
					utilities = expenses[2]
					savings = expenses[3]
					housing = expenses[4]
					debt_payments = expenses[5]
					healthcare = expenses[6]
					personal_care = expenses[7]
					food = expenses[8]
					insurance = expenses[9]
					education = expenses[10]
					entertainment = expenses[11]
					charity = expenses[12]
					taxes = expenses[13]
					miscellaneous = expenses[14]
					income = expenses[15]
					vacation_importance = expenses[16]
					daily_transportation_importance = expenses[17]
					utilities_importance = expenses[18]
					savings_importance = expenses[19]
					housing_importance = expenses[20]
					debt_payments_importance = expenses[21]
					healthcare_importance = expenses[22]
					personal_care_importance = expenses[23]
					food_importance = expenses[24]
					insurance_importance = expenses[25]
					education_importance = expenses[26]
					entertainment_importance = expenses[27]
					charity_importance = expenses[28]
					taxes_importance = expenses[29]
					miscellaneous_importance = expenses[30]
				else:
				# If no financial info exists, set default values
					vacation = 0
					daily_transportation = 0
					utilities = 0
					savings = 0
					housing = 0
					debt_payments = 0
					healthcare = 0
					personal_care = 0
					food = 0
					insurance = 0
					education = 0
					entertainment = 0
					charity = 0
					taxes = 0
					miscellaneous = 0
					income = 0
					vacation_importance = 0
					daily_transportation_importance = 0
					utilities_importance = 0
					savings_importance = 0
					housing_importance = 0
					debt_payments_importance = 0
					healthcare_importance = 0
					personal_care_importance = 0
					food_importance = 0
					insurance_importance = 0
					education_importance = 0
					entertainment_importance = 0
					charity_importance = 0
					taxes_importance = 0
					miscellaneous_importance = 0
				return render_template('update.html', year=year, month=month,time_period=time_period,financial_goal=financial_goal, vacation=vacation,
                               daily_transportation=daily_transportation, utilities=utilities,
                               savings=savings, housing=housing, debt_payments=debt_payments,
                               healthcare=healthcare, personal_care=personal_care, food=food,
                               insurance=insurance, education=education, entertainment=entertainment,
                               charity=charity, taxes=taxes, miscellaneous=miscellaneous,
                               vacation_importance=vacation_importance,
                               daily_transportation_importance=daily_transportation_importance,
                               utilities_importance=utilities_importance,
                               savings_importance=savings_importance, housing_importance=housing_importance,
                               debt_payments_importance=debt_payments_importance,
                               healthcare_importance=healthcare_importance,
                               personal_care_importance=personal_care_importance,
                               food_importance=food_importance, insurance_importance=insurance_importance,
                               education_importance=education_importance,
                               entertainment_importance=entertainment_importance,
                               charity_importance=charity_importance, taxes_importance=taxes_importance,
                               miscellaneous_importance=miscellaneous_importance,
                               income=income)
			except Exception as e:
				traceback.print_exc()
				return jsonify({'error': 'An error occurred while processing your request. Please try again later.'}), 500
			finally:
				cur.close()
				conn.close()
			
"""
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(_name_)

# Function to create SQLite table if it doesn't exist
def create_table():
    conn = sqlite3.connect('finrise.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS FinancialGoals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                income REAL DEFAULT 0,
                timePeriod INTEGER DEFAULT 0,
                financialGoal REAL DEFAULT 0,
                vacation REAL DEFAULT 0,
                vacation_importance INTEGER DEFAULT 0,
                daily_transportation REAL DEFAULT 0,
                daily_transportation_importance INTEGER DEFAULT 0,
                utilities REAL DEFAULT 0,
                utilities_importance INTEGER DEFAULT 0,
                savings REAL DEFAULT 0,
                savings_importance INTEGER DEFAULT 0,
                housing REAL DEFAULT 0,
                housing_importance INTEGER DEFAULT 0,
                debt_payments REAL DEFAULT 0,
                debt_payments_importance INTEGER DEFAULT 0,
                healthcare REAL DEFAULT 0,
                healthcare_importance INTEGER DEFAULT 0,
                personal_care REAL DEFAULT 0,
                personal_care_importance INTEGER DEFAULT 0,
                food REAL DEFAULT 0,
                food_importance INTEGER DEFAULT 0,
                insurance REAL DEFAULT 0,
                insurance_importance INTEGER DEFAULT 0,
                education REAL DEFAULT 0,
                education_importance INTEGER DEFAULT 0,
                entertainment REAL DEFAULT 0,
                entertainment_importance INTEGER DEFAULT 0,
                charity REAL DEFAULT 0,
                charity_importance INTEGER DEFAULT 0,
                taxes REAL DEFAULT 0,
                taxes_importance INTEGER DEFAULT 0,
                miscellaneous REAL DEFAULT 0,
                miscellaneous_importance INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

# Route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    form_data = request.form
    values = [form_data.get(field, 0) for field in ['Income', 'timePeriod', 'financialGoal', 'Vacation', 'daily-transportation', 'utilities', 'savings', 'housing', 'debt-payments', 'healthcare', 'personal-care', 'food', 'insurance', 'education', 'entertainment', 'charity', 'taxes', 'miscellaneous']]
    importances = [form_data.get(f'{field}-importance', 0) for field in ['Vacation', 'daily-transportation', 'utilities', 'savings', 'housing', 'debt-payments', 'healthcare', 'personal-care', 'food', 'insurance', 'education', 'entertainment', 'charity', 'taxes', 'miscellaneous']]

    # Store form data in the database
    conn = sqlite3.connect('finrise.db')
    c = conn.cursor()
    c.execute('''INSERT INTO FinancialGoals 
                 (income, timePeriod, financialGoal, vacation, vacation_importance,
                 daily_transportation, daily_transportation_importance,
                 utilities, utilities_importance, savings, savings_importance,
                 housing, housing_importance, debt_payments, debt_payments_importance,
                 healthcare, healthcare_importance, personal_care, personal_care_importance,
                 food, food_importance, insurance, insurance_importance,
                 education, education_importance, entertainment, entertainment_importance,
                 charity, charity_importance, taxes, taxes_importance,
                 miscellaneous, miscellaneous_importance)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (*values, *importances))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if _name_ == '_main_':
    create_table()  # Create table if it doesn't exist
    app.run(debug=True)

cur.execute("""SELECT vacation, daily_transportation, utilities, savings, housing, 
                                debt_payments, healthcare, personal_care, food, insurance, 
                                education, entertainment, charity, taxes, miscellaneous,  FROM UserFinancialInfo WHERE email=? AND month=? AND year=?"""",(user_email, month, year))
expenses= cur.fetchone()
print(financial_info)
if financial_info:
# If financial info exists, extract values
    vacation=expenses[0]
    daily_transportation, utilities, savings, housing, 
                                debt_payments, healthcare, personal_care, food, insurance, 
                                education, entertainment, charity, taxes, miscellaneous,
                else:
                    # If no financial info exists, set default values
                    vacation, daily_transportation, utilities, savings, housing, 
                                debt_payments, healthcare, personal_care, food, insurance, 
                                education, entertainment, charity, taxes, miscellaneous,= 0
                    financial_goal = 0
    """<script>
    function showReportSection() {
      var reportSection = document.getElementById('financialReportSection');
      reportSection.style.display = 'block'; // Show the financial report section
      return true; // Prevent form from submitting to keep page stable
    }
    </script>
    <script>
      $(document).ready(function() {
        $('#reportForm').on('submit', function(e) {
          e.preventDefault();
          $.ajax({
            url: '/report_gen', // Correct this URL if needed
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
              if (response.message) {
                $('#messageContainer').html('<div class="alert alert-warning">' + response.message + '</div>');
                $('#financialReportSection').hide(); // Hide the report section if only message
              } else {
                $('#messageContainer').empty();
                $('#financialReportSection').show().html(/* Populate with response data */);
              }
            },
            error: function() {
              $('#messageContainer').html('<div class="alert alert-danger">Error processing your request.</div>');
            }
          });
        });
      });
    </script>

  </script>



  <!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="author" content="Untree.co">
  <link rel="shortcut icon" href="favicon.png">

  <meta name="description" content="" />
  <meta name="keywords" content="bootstrap, bootstrap4" />

  <!-- Bootstrap CSS -->
  <link href="/static/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
  <link href="/static/css/tiny-slider.css" rel="stylesheet">
  <link href="/static/css/style.css" rel="stylesheet">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

  <title>FinRise</title>
</head>

<body>
  <!-- Start Header/Navigation -->
  <nav class="custom-navbar navbar navbar-expand-md navbar-dark bg-dark" aria-label="Furni navigation bar">
    <div class="container">
      <a class="navbar-brand" href="index.html">FinRise<span>.</span></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsFurni" aria-controls="navbarsFurni" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarsFurni">
        <ul class="custom-navbar-nav navbar-nav ms-auto mb-2 mb-md-0">
          <li class="nav-item active" id="homeNavItem">
            <a class="nav-link" href="/">Home</a>
          </li>
          <li class="nav-item" id="inputNavItem">
            <a class="nav-link" href="/input">Expense Entry</a>
          </li>
          <li class="nav-item" id="servicesNavItem">
            <a class="nav-link" href="/update">Expense Updation</a>
          </li>
          <li class="nav-item" id="contactNavItem">
            <a class="nav-link" href="/report">Report</a>
          </li>
        </ul>

        <ul class="custom-navbar-cta navbar-nav mb-2 mb-md-0 ms-5">
          <li id="userContainer"></li>
          {% if not session['email'] %}
            <li><a class="nav-link" href="#"><img src="/static/images/user.svg"></a></li><!-- Display user icon -->
          {% else %}
            <li><a class="nav-link" href="#"><i class="fas fa-user"></i> {{ session['email'] }}</a></li> <!-- Display email -->
            <li><a class="nav-link" href="/logout">Logout</a></li> <!-- Logout button -->
          {% endif %}
        </ul>
      </div>
    </div>
  </nav>
  <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Report</title>
    <style>
      
    #financialReportSection {
      display: none; /* Initially hide the financial report section */
    }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
  <div class="container mt-5">
    <form action="/report_gen" method="POST" id="reportForm"> 
      <div class="row">
        <div class="col-md-3">
          <div class="form-group">
            <label for="month">Month:</label>
            <select id="month" name="month" class="form-control">
              <option value="January">January</option>
              <option value="February">February</option>
              <!-- More months -->
            </select>
          </div>
        </div>
        <div class="col-md-3">
          <div class="form-group">
            <label for="year">Year:</label>
            <select id="year" name="year" class="form-control">
              {% for year in range(2024, 2034) %}
              <option value="{{ year }}">{{ year }}</option>
              {% endfor %}
            </select>
          </div>
        </div>
        <div class="col-md-3">
          <button type="button" class="btn btn-secondary me-2" id="reportbtn">Show Report</button>
        </div>
      </div>
    </form>
    <div id="messageContainer"">
        <div id="financialReportSection" >
            <br>
            <h1>Financial Report for {{ month }} {{ year }}</h1>
                <br>
                <h2>User Financial Information</h2>
                <table style="width: 40%;">
                    <thead>
                        <tr>
                            <th>Financial Goal</th>
                            <th>Time Period</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ financial_info[1] }}</td> <!-- Financial Goal -->
                            <td>{{ financial_info[2] }}</td> <!-- Time Period -->
                        </tr>
                    </tbody>
                </table>
                    <br>
                    <h2>Expenses Data</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Income</th>
                                <th>Vacation</th>
                                <th>Daily Transportation</th>
                                <th>Utilities</th>
                                <th>Savings</th>
                                <th>Housing</th>
                                <th>Debt Payments</th>
                                <th>Healthcare</th>
                                <th>Personal Care</th>
                                <th>Food</th>
                                <th>Insurance</th>
                                <th>Education</th>
                                <th>Entertainment</th>
                                <th>Charity</th>
                                <th>Taxes</th>
                                <th>Miscellaneous</th>
                                <!-- Add remaining expense columns here -->
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in expenses_data %}
                                <tr>
                                    <td>{{ row[1] }}</td> <!-- Income -->
                                    <td>{{ row[4] }}</td> <!-- Vacation -->
                                    <td>{{ row[5] }}</td> <!-- Daily Transportation -->
                                    <td>{{ row[6] }}</td> <!-- Utilities -->
                                    <td>{{ row[7] }}</td> <!-- Savings -->
                                    <td>{{ row[8] }}</td> <!-- Housing -->
                                    <td>{{ row[9] }}</td> <!-- Debt Payments -->
                                    <td>{{ row[10] }}</td> <!-- Healthcare -->
                                    <td>{{ row[11] }}</td> <!-- Personal Care -->
                                    <td>{{ row[12] }}</td> <!-- Food -->
                                    <td>{{ row[13] }}</td> <!-- Insurance -->
                                    <td>{{ row[14] }}</td> <!-- Education -->
                                    <td>{{ row[15] }}</td> <!-- Entertainment -->
                                    <td>{{ row[16] }}</td> <!-- Charity -->
                                    <td>{{ row[17] }}</td> <!-- Taxes -->
                                    <td>{{ row[18] }}</td> <!-- Miscellaneous -->
                                    <!-- Add remaining expense fields here -->
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    <div>
                      <br>
                      {% if max_category %}
                          <h2>Expense category in which the spending can be reduced is {{ max_category }}.</h2>
                      {% else %}
                          <h2>No overspending.</h2>
                      {% endif %}
                      <br>
                      {% if remaining > 0 %}
                          <h2>Rs {{ remaining }} remaining to achieve.</h2>
                      {% elif remaining == 0 %}
                          <h2>Financial goal achieved!</h2>
                      {% else %}
                          <h2>Financial goal achieved!</h2>
                          <h2>Excess savings: Rs {{ -remaining }}</h2>
                      {% endif %}
                  </div>
          </div>
  </div>
  <script>
    document.getElementById('reportbtn').addEventListener('click', function() {
        var month = document.getElementById('month').value;
        var year = document.getElementById('year').value;
        var messageContainer = document.getElementById('messageContainer');
    
        // Optionally, check if month and year are selected
        if (month !== '' && year !== '') {
            // Display the message container when a month and year are selected
            messageContainer.style.display = 'block';
        } else {
            alert('Please select a month and a year.');
        }
    });
    </script>
    
  <script src="/static/js/bootstrap.bundle.min.js"></script>
  <script src="/static/js/tiny-slider.js"></script>
  <script src="/static/js/custom.js"></script>
</body>
</html>
