from flask import Flask, request, render_template, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhinav@2787",
    database="student_details"
)
cursor = db.cursor()

@app.route('/')
def home():
    return redirect('/submit')

@app.route('/submit', methods=['GET', 'POST'])
def student_form():
    if request.method == 'POST':
        roll = request.form['roll_number']
        name = request.form['name']
        age = request.form['age']
        branch = request.form['branch']
        email = request.form['email']
        gender = request.form['gender']
        address = request.form['address']

        if roll and name and age and branch and email and gender and address:
            try:
                sql = """
                    INSERT INTO students 
                    (roll, name, age, branch, email, gender, address) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (roll, name, age, branch, email, gender, address))
                db.commit()
                return redirect('/students')
            except Exception as e:
                db.rollback()
                return f"Error: {str(e)}"
        else:
            return "Please fill all fields."

    return render_template('studentdatabase.html')

@app.route('/students')
def show_students():
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return render_template('studentdatabase.html', students=students)
    except Exception as e:
        return f"Error fetching students: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
