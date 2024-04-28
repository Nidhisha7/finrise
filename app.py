import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session,redirect,flash
import traceback
import sqlite3

app = Flask(__name__)
app.secret_key = 'key'

# Function to connect to the SQLite database
def connect_db():
	return sqlite3.connect('database.db')

@app.route('/')
def home():
   return render_template('main.html')
   
@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		# Get the form data from the request
		name = request.form.get('Username')
		email = request.form.get('Email')
		password = request.form.get('Password')

		# Connect to the database
		conn = connect_db()
		cur = conn.cursor()

		try:
			# Check if the email already exists in the database
			cur.execute("SELECT email FROM user WHERE email=?", (email,))
			result = cur.fetchone()
			if result:  # If the email already exists
				error_message = 'Account already exists'
				return render_template('SignUp.html', error=error_message)
			else:
				# Insert the new user into the database
				cur.execute("INSERT INTO user (Username, email, password) VALUES (?, ?, ?)", (name, email, password))
				conn.commit()  # Commit the transaction to save changes
				success_message = 'Signup successful'
				return render_template('SignUp.html', error=success_message)
		except Exception as e:
			# If any error occurs, rollback changes and return an error message
			conn.rollback()
			error_message = 'Error: ' + str(e)
			print(error_message)  # Log the error message
			return render_template('SignUp.html', error=error_message)
		finally:
			# Close the cursor and database connection
			cur.close()
			conn.close()
	else:
		# Handle GET request for signup page
		return render_template('SignUp.html')


@app.route('/logout')
def logout():
	# Clear the session data
	session.clear()
	# Redirect the user to the login page
	return redirect(url_for('home'))
@app.route('/login', methods=['GET', 'POST'])
def login_api():
	if request.method == 'POST':
		# Get the form data from the request
		email = request.form.get('email')
		password = request.form.get('password')

		try:
			# Connect to the database
			conn = connect_db()
			cur = conn.cursor()

			# Check if the email and password match a record in the database
			cur.execute("SELECT email FROM user WHERE email=? AND password=?", (email, password))
			result = cur.fetchone()
			if result:  # If the email and password are correct
				# Store the email in the session to keep the user logged in
				session['email'] = email # Store user's email in the session
				# Close cursor and commit changes
				cur.close()
				conn.commit()
				conn.close()
				return redirect(url_for('home'))  # Redirect to the home page after successful login
			else:
				error_message = 'Invalid email or password'
				return render_template('login.html', error=error_message)
		except Exception as e:
			# If any error occurs, return an error message
			error_message = 'An error occurred: ' + str(e)
			return render_template('login.html', error=error_message)
	else:
		# Handle GET request for login page
		return render_template('login.html')
import traceback
@app.route('/input', methods=['POST', 'GET'])
def input():
    if 'email' in session:  # Ensure the user is logged in
        email = session['email']  # Assuming 'email' is stored in session upon login
        conn = connect_db()
        cur = conn.cursor()
        # Check for existing financial info on GET request
        if request.method == 'GET':
            cur.execute("SELECT time_period, financial_goal FROM UserFinancialInfo WHERE email=?", (email,))
            #cur.execute("SELECT time_period, financial_goal FROM UserFinancialInfo ")
            financial_info = cur.fetchone()
            if financial_info:
                # Data exists, so pass it back to the template
                time_period, financial_goal = financial_info
                return render_template('input.html', time_period=time_period, financial_goal= financial_goal)
            else:
                # No data, render the page normally for a new entry
                return render_template('input.html')

        if request.method == 'POST':
            try:
                # Extract form data
                email = session['email']
                income = float(request.form.get('income', 0) or 0)
                month = request.form.get('month')
                year = request.form.get('year')
                time_period = int(request.form.get('timePeriod', 0))  # Corrected field name
                financial_goal = float(request.form.get('financialGoal', 0))
                print(year)
				
                # Insert or update financial info
                cur.execute("SELECT COUNT(*) FROM UserFinancialInfo WHERE email=?", (email,))
                if cur.fetchone()[0] == 0:
                    # Insert new financial info
                    cur.execute("INSERT INTO UserFinancialInfo (email, time_period, financial_goal) VALUES (?, ?, ?)",
                                (email, time_period, financial_goal))
                else:
                    # Update existing financial info
                    cur.execute("UPDATE UserFinancialInfo SET time_period=?, financial_goal=? WHERE email=?",
                                (time_period, financial_goal, email))
                cur.execute("SELECT COUNT(*) FROM Expenses WHERE email=? AND month=? AND year=?", (email, month, year))
                if cur.fetchone()[0] > 0:
                    flash('Records already exist for this month and year.', 'info')
                    return redirect(url_for('input'))
                # Handle expenses part of the form
                expenses = {key:request.form[key] if request.form[key] != '' else 0.0 for key in request.form if key not in ['income', 'month', 'year', 'timePeriod', 'financialGoal']}
                importances = {key.replace('-importance', ''): int(request.form.get(key, 0)) for key in request.form if key.endswith('-importance')}
                # Create a tuple containing all the values for the INSERT statement
                print("Month",month)
                print("Year",year)
                t = (session['email'], income, month, year) + tuple(expenses.get(key, 0) for key in ['Vacation', 'daily-transportation', 'utilities', 'savings',
                                                    'housing', 'debt-payments', 'healthcare', 'personal-care',
                                                    'food', 'insurance', 'education', 'entertainment',
                                                    'charity', 'taxes', 'miscellaneous']) + tuple(importances.get(key, 0) for key in ['Vacation', 'daily-transportation', 'utilities', 'savings',
                                                       'housing', 'debt-payments', 'healthcare', 'personal-care',
                                                       'food', 'insurance', 'education', 'entertainment',
                                                      'charity', 'taxes', 'miscellaneous'])
                print(t)

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
                flash('Your expenses have been successfully submitted.', 'success')
                return redirect(url_for('input'))  # Redirect to prevent form re-submission
            except Exception as e:
                traceback.print_exc()
                conn.rollback()
                return jsonify({'error': 'An error occurred while processing your request. Please try again later.'}), 500
            finally:
                cur.close()
                conn.close()
    else:
        return jsonify({'error': 'Unauthorized access. Please log in.'})
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    if 'email' in session:  # Ensure the user is logged in
        email = session['email']
        month = request.args.get('month')
        year = int(request.args.get('year'))
        conn = connect_db()
        cur = conn.cursor()
        try:
            # Fetch expenses based on the month and year provided in the query parameters
            cur.execute("SELECT financial_goal,time_period FROM UserFinancialInfo WHERE email=? ", (email,))
            expenses = cur.fetchone()  # Assume this returns a list of expense records
            print("Expense",expenses)
            if expenses:
                return jsonify(expenses)  # Return expenses as JSON
            else:
                return jsonify({'message': 'No expenses found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({'error': 'Unauthorized'}), 401
#@app.route('/update', methods=['GET', 'POST'])
# def update_expense():
# 	if 'email' in session:
# 		user_email = session['email']
# 		print('post')
# 		if request.method == 'POST':
# 			print('mail')
# 			conn = connect_db()
# 			cur = conn.cursor()    
# 			try:
# 				month = str(request.form['month'])
# 				year = request.form['year']
# 				print("month;",month)
# 				print('year:',year)
# 			# 	income = float(request.form.get('income', 0) or 0)
# 			# 	month = str(request.form.get('month', 'null'))
# 			# 	year = request.form.get('year', 'null')
# 			# 	print("Month :",month)
# 			# 	print("Year :",year)
# 			# 	cur.execute("SELECT * FROM Expenses WHERE email = ? AND month = ? AND year = ?", (session['email'], month, year))
# 			# 	existing_expense = cur.fetchone()
# 			# 	if existing_expense:
# 			# 		return jsonify({'message': 'Expense entry already exists for the specified month and year.'}), 200
# 			# 	time_period = int(request.form.get('timePeriod', 0)) 
# 			# 	financial_goal = float(request.form.get('financialGoal', 0))
# 			# 	conn.commit()
# 			# 	expenses = {key: float(request.form[key]) if request.form[key] != '' else 0.0 for key in request.form if key not in ['income', 'month', 'year', 'timePeriod', 'financialGoal']}
# 			# 	importances = {key.replace('-importance', ''): int(request.form.get(key, 0)) for key in request.form if key.endswith('-importance')}
# 			# 	t = (session['email'], income, month, year) + tuple(expenses.get(key, 0) for key in ['Vacation', 'daily-transportation', 'utilities', 'savings',
# 			# 										'housing', 'debt-payments', 'healthcare', 'personal-care',
# 			# 										'food', 'insurance', 'education', 'entertainment',
# 			# 										'charity', 'taxes', 'miscellaneous']) + tuple(importances.get(key, 0) for key in ['Vacation', 'daily-transportation', 'utilities', 'savings',
# 			# 										   'housing', 'debt-payments', 'healthcare', 'personal-care',
# 			# 										   'food', 'insurance', 'education', 'entertainment',
# 			# 										   'charity', 'taxes', 'miscellaneous'])
# 			# 	print(t)
# 			# 	cur.execute('''INSERT INTO Expenses 
# 			#    (email, income, month, year,
# 			# 	vacation, daily_transportation, utilities, savings, housing, 
# 			# 	debt_payments, healthcare, personal_care, food, insurance, 
# 			# 	education, entertainment, charity, taxes, miscellaneous,
# 			# 	vacation_importance, daily_transportation_importance, utilities_importance, 
# 			# 	savings_importance, housing_importance, debt_payments_importance, 
# 			# 	healthcare_importance, personal_care_importance, food_importance, 
# 			# 	insurance_importance, education_importance, entertainment_importance, 
# 			# 	charity_importance, taxes_importance, miscellaneous_importance) 
# 			#    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', t)
# 			# 	conn.commit()
# 				message = "Data successfully inserted into the table." 
# 			except Exception as e:
# 				traceback.print_exc()
# 				conn.rollback()
# 				return jsonify({'error': 'An error occurred while processing your request. Please try again later.'}), 500
# 			finally:
# 				cur.close()
# 				conn.close()
# 			return jsonify({'message': message}), 200
# 		return render_template('update.html')
		
# 	else:
# 		return jsonify({'error': 'Unauthorized access. Please log in.'})

@app.route('/report_gen',methods=['POST','GET'])
def generate_report():
	# Retrieve data from the database based on the provided month, year, and user email
	if 'email' in session:
		user_email = session['email']
		# month = 'January'
		# year = 2024
		# financial_info = [1,2,2,3]
		# expenses_data = [12,23,3,3]
		# max_category = "test"
		# remaining = 809.23
		print("In Session")
		print("Request method:", request.method)
		 
		if request.method=='GET':
			print("Inside Post")
			conn = connect_db()
			cur = conn.cursor()
			try:
				month = str(request.form.get('month'))
				year = request.form.get('year')
				print("Month",month)
				#Retrieve financial information
				cur.execute('''SELECT email, financial_goal, time_period FROM UserFinancialInfo WHERE email=?''', (user_email,))
				financial_info = cur.fetchone()
				print("financial_info", financial_info)
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
				# if not expenses_data:
				# 	return render_template('report.html', month=month, year=year, message="No data available for the selected month and year")
				cur.execute('''SELECT income FROM Expenses where email=? AND month=? AND year=?''', (user_email, month, year))
				income = cur.fetchone()[0]
				print(income)
				

				# for essential category
				cur.execute('''SELECT housing, utilities, daily_transportation, food, debt_payments, healthcare, insurance, taxes FROM Expenses where email=? AND month=? AND year=?''', (user_email, month, year))
				essential_data = cur.fetchone()

				cur.execute('''SELECT housing_importance, utilities_importance, daily_transportation_importance, food_importance, debt_payments_importance, healthcare_importance, insurance_importance, taxes_importance FROM Expenses where email=? AND month=? AND year=?''', (user_email, month, year))
				essential_imp = cur.fetchone()
			
			# for savings category
				cur.execute('''SELECT savings, education, charity FROM Expenses where email=? AND month=? AND year=?''', (user_email, month, year))
				savings_data = cur.fetchone()
				cur.execute('''SELECT savings_importance, education_importance, charity_importance FROM Expenses where email=? AND month=? AND year=?''', (user_email, month, year))
				savings_imp = cur.fetchone()

			# for personal category
				cur.execute('''SELECT entertainment, personal_care, miscellaneous, vacation FROM Expenses where email=? AND month=? AND year=?''', (user_email, month, year))
				personal_data = cur.fetchone()
				cur.execute('''SELECT entertainment_importance, personal_care_importance, miscellaneous_importance, vacation_importance FROM Expenses where email=? AND month=? AND year=?''', (user_email, month, year))
				personal_imp = cur.fetchone()  

			# Set limits
				essential_limit = 0.6 * income
				savings_limit = 0.2 * income
				personal_limit = 0.2 * income

			# Determine the category with the highest spending and select the attribute
				if sum(essential_data) > essential_limit:
					essential_imp_filtered = [imp for imp, expense in zip(essential_imp, essential_data) if expense != 0]
					essential_data_filtered = [expense for expense in essential_data if expense != 0]
					essential_category = [expense for imp, expense in zip(essential_imp_filtered, essential_data_filtered) if imp == min(essential_imp_filtered)]
					max_index = essential_data.index(max(essential_category))
					essential = ['housing', 'utilities', 'daily_transportation', 'food', 'debt_payments', 'healthcare', 'insurance', 'taxes']                    
					max_category = savings_attributes[max_index]

				elif sum(personal_data) > personal_limit:
					personal_imp_filtered = [imp for imp, expense in zip(personal_imp, personal_data) if expense != 0]
					personal_data_filtered = [expense for expense in personal_data if expense != 0]
					personal_category = [expense for imp, expense in zip(personal_imp_filtered, personal_data_filtered) if imp == min(personal_imp_filtered)]
					max_index = personal_data.index(max(personal_category))
					personal_attributes = ['entertainment', 'personal_care', 'miscellaneous', 'vacation']
					max_category = personal_attributes[max_index]
					
				elif sum(savings_data) > savings_limit:
					savings_imp_filtered = [imp for imp, expense in zip(savings_imp, savings_data) if expense != 0]
					savings_data_filtered = [expense for expense in savings_data if expense != 0]
					savings_category = [expense for imp, expense in zip(savings_imp_filtered, savings_data_filtered) if imp == min(savings_imp_filtered)]
					max_index = savings_data.index(max(savings_category))
					savings_attributes = ['savings', 'education', 'charity']
					max_category = savings_attributes[max_index]
				
				# Fetch the sum of savings from the Expenses table
				cur.execute("""SELECT SUM(savings) FROM Expenses WHERE email=?""", (user_email,))
				sav = cur.fetchone()
				total_savings = sav[0] if sav else 0.0  # Use 0.0 if no savings are found
				remaining = financial_goal - total_savings
				return  redirect('report',month=month,year=year, financial_info=financial_info,expenses_data=expenses_data,
                               max_category=max_category, remaining=remaining)
			except Exception as e:
				# Log the exception and traceback
				traceback.print_exc()
				print("Error")
				return jsonify({'error': 'An error occurred while retrieving the report data. Please try again later.'})
			finally:
				# Close the cursor and database connection
				cur.close()
				conn.close()
		
		return render_template('report.html',month=month,year=year, financial_info=financial_info,expenses_data=expenses_data,
                               max_category=max_category, remaining=remaining)
	else:
		return jsonify({'error': 'Unauthorized access. Please log in.'})
	
"""
@app.route('/update/<int:year>/<string:month>', methods=['POST','GET'])
def update_expenses(year, month):
	if 'email' in session:
		conn = connect_db()
		cur = conn.cursor()
		try:
			# Get form data from the request
			# Extract expense values from the form data
			expenses = {key: float(request.form[key]) if request.form[key] != '' else 0.0 for key in request.form if key not in ['month', 'year']}
			importances = {key.replace('-importance', ''): int(request.form.get(key, 0)) for key in request.form if key.endswith('-importance')}
		
			# Update existing expense values in the database
			cur.execute('''UPDATE Expenses 
						   SET vacation = ?, daily_transportation = ?, utilities = ?, savings = ?, housing = ?, debt_payments = ?, 
							   healthcare = ?, personal_care = ?, food = ?, insurance = ?, education = ?, entertainment = ?, 
							   charity = ?, taxes = ?, miscellaneous = ?,
							   vacation_importance = ?, daily_transportation_importance = ?, utilities_importance = ?, savings_importance = ?,
							   housing_importance = ?, debt_payments_importance = ?, healthcare_importance = ?, personal_care_importance = ?,
							   food_importance = ?, insurance_importance = ?, education_importance = ?, entertainment_importance = ?,
							   taxes_importance = ?, charity_importance = ?, miscellaneous_importance = ?
						   WHERE email = ? AND month = ? AND year = ?''',
						(expenses.get('Vacation', 0), expenses.get('daily-transportation', 0), expenses.get('utilities', 0),
						 expenses.get('savings', 0), expenses.get('housing', 0), expenses.get('debt-payments', 0),
						 expenses.get('healthcare', 0), expenses.get('personal-care', 0), expenses.get('food', 0),
						 expenses.get('insurance', 0), expenses.get('education', 0), expenses.get('entertainment', 0),
						 expenses.get('charity', 0), expenses.get('taxes', 0), expenses.get('miscellaneous', 0),
						 importances.get('Vacation', 0), importances.get('daily-transportation', 0), importances.get('utilities', 0),
						 importances.get('savings', 0), importances.get('housing', 0), importances.get('debt-payments', 0),
						 importances.get('healthcare', 0), importances.get('personal-care', 0), importances.get('food', 0),
						 importances.get('insurance', 0), importances.get('education', 0), importances.get('entertainment', 0),
						 importances.get('taxes', 0), importances.get('charity', 0), importances.get('miscellaneous', 0),
						 session.get('email', ''), month, year))
			conn.commit()

			# Redirect to the report page after successful update
			return redirect(url_for('report', year=year, month=month)) # Pass month and year here
		except Exception as e:
			# Log the exception and traceback
			traceback.print_exc()
			# If any error occurs, rollback changes and return an error message
			conn.rollback()
			return jsonify({'error': 'An error occurred while processing your request. Please try again later.'}), 500
		finally:
			# Close the cursor and database connection
			cur.close()
			conn.close()
	else:
		return jsonify({'error': 'User not logged in.'}), 401

@app.route('/check_entry', methods=['GET','POST'])
def check_entry():
	try:
		# Get the month and year from the request query parameters
		month = request.args.get('month')
		year = request.args.get('year')

		# Perform the necessary checks to determine if the entry exists
		# For example, query your database to check if an entry exists for the given month and year
		# Replace the following line with your actual database query
		entry_exists = check_entry_in_database(month, year)

		# Return a response indicating whether the entry exists or not
		if entry_exists:
			return jsonify({'exists': True})
		else:
			return jsonify({'exists': False})

	except Exception as e:
		# Log the exception and return an error message
		print(e)
		return jsonify({'error': 'An error occurred while processing your request.'}), 500

# Function to check if an entry exists in the database
def check_entry_in_database(month, year):
	# Implement your database query here
	# Return True if the entry exists, False otherwise
	# This is just a placeholder function, replace it with your actual implementation
	return False  # Replace with your actual implementation
"""
if __name__ == '__main__':
	app.run(debug=True,port=5000)
