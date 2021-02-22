from flask import Flask,render_template,redirect,logging,session,url_for,flash
import sqlite3
from createdict import CreateDict
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import random

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Get Key')

class FeedbackForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired()])
    content = StringField('Başlık', validators=[DataRequired()])
    desc = StringField('Açıklama', validators=[DataRequired()])
    submit = SubmitField('Get Key')

def get_random_string():
    sample_letters = ',0123456789:;<>?@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    result_str = ''.join((random.choice(sample_letters) for i in range(16)))
    return result_str

app = Flask(__name__)
app.config['SECRET_KEY'] = "you-will-never-guest:)"
DB_PATH = "database.db"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/newkey', methods = ["GET","POST"])
def demokey():
    form = LoginForm()
    if form.validate_on_submit():
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()

        cursor.execute("SELECT * FROM allkeys")
        data = cursor.fetchall()
        firstT = True
        for i in range(len(data)):
            if(data[i][1] == form.email.data):
                firstT = False
                flash("Daha önceden demo anahtar aldınız.")
                return redirect('/')
        if(firstT):
            key = get_random_string()
            print(form.email.data, form.password.data, key)
            exe = "INSERT INTO allkeys (email,password,key,mcount) VALUES ('{}','{}','{}',{})".format(form.email.data,form.password.data,key,15)
            cursor.execute(exe)
            con.commit()
            flash("15 Mesaj Hakkı olan Anahtarınız : "+ str(key))
            return redirect('/')

    return render_template("demo.html", form = form)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/feedback', methods = ["GET","POST"])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        print(form.content,form.email,form.desc)
    return render_template("demo.html",form = form)

@app.route('/wp/<key>')
def wp(key):
    c_id = None
    info = False
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    if (key[0] == "_" and key[-1] == "_"):
        info = True
        key = key[:-1]
        key = key[1:]


    cursor.execute("SELECT * FROM allkeys")
    data = cursor.fetchall()
    
    for i in range(len(data)):
        data[i] = list(data[i])
    for a in range(len(data)):
        if str(key) == str(data[a][4]):
            print(data[a])
            c_id = data[a][0]
            id = int(a)
    try:
        if id == "":
            pass
    except:
        info = False
    if (info == True):
        return CreateDict("info",data[id])
    if c_id is not None:
        try:
            cursor.execute("UPDATE allkeys SET mcount = mcount - 1 WHERE id ='{}'".format(c_id))
        except sqlite3.OperationalError:
            return CreateDict("database_locked")
        if(int(data[id][5]) <= 0):
            return CreateDict("no_message_count",data[id])
        con.commit()
        return CreateDict("sent",data[id])
    else:
        return CreateDict("no_auth_key")

if __name__ == '__main__':
    app.run(debug=True)