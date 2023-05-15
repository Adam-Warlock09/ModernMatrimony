from flask import Flask,redirect,url_for,render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__) 

# configure db
app.config['MYSQL_HOST'] = os.getenv("HOST")
app.config['MYSQL_PASSWORD'] = os.getenv("PASSWORD")
app.config['MYSQL_USER'] = os.getenv("USERNAME")
app.config['MYSQL_DB'] = os.getenv("DATABASE")

mysql = MySQL(app)

@app.route('/')
def display():
    return render_template('index.html')

# accept submit btn
@app.route('/result', methods=['POST','GET'])
def submit():
    cur = mysql.connection.cursor()
    s = tuple(float(x) for x in request.form.getlist('inp'))
    cur.execute(f"INSERT INTO marks(science, maths, english, computer) VALUES {s}")
    mysql.connection.commit()
    cur.close()
    if request.form.get('result'):  #check from which source request came
        return render_template('result.html',marks=sum(s)/4)
    else:
        return render_template('percent.html',d = zip(['Science','Maths','English','Computer'],list(s)))

@app.route('/view')
def view():
    cur = mysql.connection.cursor()
    result_Value = cur.execute("SELECT * FROM  marks")
    if result_Value > 0:
        userDetails = cur.fetchall()
        return render_template('marks.html', marks=userDetails)


if __name__ =='__main__':
    app.run(debug=False)