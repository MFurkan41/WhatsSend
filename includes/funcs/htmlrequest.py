import mysql.connector
import time

def HtmlRequest(key,info):
    db = mysql.connector.connect(host = "db4free.net",
                            user = "id15985185_wpu1",
                            passwd = "*NC5@P#me(xQDlpFO2lL",
                            database = "id15985185_wpdb1")
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE mkey = {}".format(key))
    try:
        data = cur.fetchall()[0]
    except IndexError:
        return {"error_message":"no_auth_key"}
    if data["mcount"] == 0:
        return {"error_message":"no_message_count"}
    data["error_message"] = ""

    if(info == False):
        data["mcount"] -= 1
        cur.execute("UPDATE users SET mcount={} WHERE mkey={}".format(data["mcount"],key))
        db.commit()
    return data
    
#print(HtmlRequest("1245",False))
