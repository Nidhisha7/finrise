import sqlite3

conn=sqlite3.connect("database.db")
cur=conn.cursor()
cur.execute('''INSERT INTO Expenses(email,month,year,income,housing,utilities,daily_transportation,food,debt_payments,healthcare,insurance,taxes, housing_importance,utilities_importance,daily_transportation_importance,food_importance,debt_payments_importance,healthcare_importance,insurance_importance,taxes_importance,savings,education,charity,savings_importance,education_importance,charity_importance,entertainment,personal_care,miscellaneous,vacation,entertainment_importance,personal_care_importance,miscellaneous_importance,vacation_importance) VALUES ('nidhin1@slk.com','January','2024',10000,10000,1500,200,500,0,0,300,5000,3,2,1,2,1,1,1,1,10000,3000,200,3,1,2,10000,5000,1000,0,1,2,1,1)''')
conn.commit()
cur.execute("""INSERT INTO UserFinancialInfo VALUES('nidhin1slk@gmail.com',12,50000)""")
"""
cur.execute("CREATE TABLE IF NOT EXISTS user( Username TEXT,email TEXT PRIMARY KEY,password TEXT)")
cur.execute("SELECT * FROM user")
cur.execute('''CREATE TABLE IF NOT EXISTS Expenses(
                email TEXT ,
                income REAL,
                month TEXT,
                year INTEGER,
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
            ,FOREIGN KEY (email) REFERENCES user(email)
                )''')

cur.execute('''CREATE TABLE UserFinancialInfo (
    email TEXT PRIMARY KEY,
    financial_goal FLOAT,
    time_period INTEGER,
    FOREIGN KEY (email) REFERENCES Users(email)
);''')


"""



cur.execute("SELECT income FROM Expenses WHERE email='nidhishasdharan@gmail.com' AND month='January' AND year=2024")

# Fetch all rows from the result set
rows = cur.fetchone()

# Print the heading

# Close the cursor and connection
cur.close()
conn.close()
