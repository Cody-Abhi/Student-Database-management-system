from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhinav@2787",  # change if your MySQL has password
    database="studentdb"
)
cursor = conn.cursor()

# Home Page - Add Student
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['roll_number'],
        request.form['name'],
        request.form['age'],
        request.form['branch'],
        request.form['email'],
        request.form['gender'],
        request.form['address']
    )
    cursor.execute("INSERT INTO studentsinfo (roll_number, name, age, branch, email, gender, address) VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
    conn.commit()
    return redirect('/studentslist')

# View all students
@app.route('/studentslist')
def students():
    cursor.execute("SELECT * FROM studentsinfo")
    students = cursor.fetchall()
    return render_template('view.html', students=students)

# Search Student
@app.route('/search', methods=['GET', 'POST'])
def search():
    student = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        query = f"""SELECT * FROM studentsinfo WHERE 
                    roll_number LIKE %s OR
                    name LIKE %s OR
                    email LIKE %s OR
                    branch LIKE %s"""
        cursor.execute(query, tuple(['%'+keyword+'%']*4))
        student = cursor.fetchall()
    return render_template('search.html', students=student)

# Delete Student
@app.route('/delete', methods=['POST'])
def delete():
    keyword = request.form['keyword']
    query = """DELETE FROM studentsinfo WHERE 
               roll_number LIKE %s OR
               name LIKE %s OR
               email LIKE %s OR
               branch LIKE %s"""
    cursor.execute(query, tuple(['%'+keyword+'%']*4))
    conn.commit()
    return redirect('/studentslist')

# Update Page


# @app.route('/update_form', methods=['POST'])
# def update_form():
#     roll_number = request.form.get('roll_number')

#     cursor.execute("SELECT * FROM studentsinfo WHERE roll_number=%s", (roll_number,))
#     student = cursor.fetchone()
#     return render_template("update.html", student=students)


# @app.route('/update', methods=['POST'])
# def update():
#     roll_number = request.form.get('roll_number')
#     name = request.form.get('name')
#     branch = request.form.get('branch')
#     gender = request.form.get('gender')
#     address = request.form.get('address')
#     age = request.form.get('age')
#     cursor.execute("UPDATE studentsinfo SET name=%s, branch=%s, gender=%s, address=%s, age=%s WHERE roll_number=%s",
#                    (name, age, branch, gender, address, roll_number))
#     conn.commit()
#     return redirect('/studentslist')

if __name__ == "__main__":
    app.run(debug=True)
