from flask import Flask,render_template,redirect,logging,session,url_for
import sqlite3
from createdict import CreateDict

app = Flask(__name__)
DB_PATH = "database.db"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")


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
        if str(key) == str(data[a][3]):
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
        if(int(data[id][4]) <= 0):
            return CreateDict("no_message_count",data[id])
        con.commit()
        return CreateDict("sent",data[id])
    else:
        return CreateDict("no_auth_key")

if __name__ == '__main__':
    app.run(debug=True)