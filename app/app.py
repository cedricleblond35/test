# from cgitb import html
# from numpy import imag
import mysql.connector  # pip install mysql-connector-python
# import pickle
import requests
from camera import VideoCamera
from model.admin import Admin
import hashlib  # MD5
from flask import Flask, render_template, redirect, request, session, Response, url_for
from flask_session import Session
import flask_monitoringdashboard as dashboard

# from bs4 import BeautifulSoup


# import unittest

app = Flask(__name__)

# monotoring
dashboard.config.init_from(file='config.cfg')  # In order to configure the Dashboard with a configuration-file,
# dashboard.bind(app) # add monotoring

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

s = requests.Session()


def connector():
    try:
        cnx = mysql.connector.connect(
            host="0.0.0.0",
            port=3310,
            user="root",
            passwd="MYsql",
            database="ASL")
    except mysql.connector.Error as e:
        print("Error code:", e.errno)         # error number
        print("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print("Error message:", e.msg)       # error message
        print("Error:", e)                   # errno, sqlstate, msg values
        s = str(e)
        print("Error:", s)                   # errno, sqlstate, msg values


    return cnx.cursor()


def identification(email, pwd):

    try:
        cnx = mysql.connector.connect(
                    host="0.0.0.0",
                    port=3310,
                    user="root",
                    passwd="MYsql",
                    database="ASL")
        cursor = cnx.cursor()
        requete = 'SELECT name, lastname FROM user WHERE email="' + email + '" and password="' + pwd + '"'
        cursor.execute(requete)   # Syntax error in query
        
        res = cursor.fetchall()
        print("quantite :", len(res) )
        for raw in res:
            print (raw[0], raw[1])



        # for (name, lastname) in cursor:
        #     print("11111111111111name :", name, lastname)


        cnx.close()
    except mysql.connector.Error as e:
        print("Error code:", e.errno)         # error number
        print("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        print("Error message:", e.msg)       # error message
        print("Error:", e)                   # errno, sqlstate, msg values
        s = str(e)
        print("Error:", s)                   # errno, sqlstate, msg values










    cnx = mysql.connector.connect(
            host="0.0.0.0",
            port=3310,
            user="root",
            passwd="MYsql",
            database="ASL")

    cur = cnx.cursor()
    
    requete = 'SELECT * FROM user WHERE email="' + email + '" and password="' + pwd + '"'
    print(requete)
    res = cur.execute(requete)
    for (name, lastname) in cur:
        print("name 222222222:", name, lastname)




def createUser(cur, name, lastname, email, pwd, role):
    requete = 'INSERT INTO user (name, lastname, email, password, role_id) VALUES ("' + name + '","' + lastname + '","' + email + '","' + pwd + '","' + role + '")'
    cur.execute(requete)
    cur.commit()


def updateUser(cur, id, name, lastname, email, pwd, role):
    requete = 'UPDATE user SET name="' + name + '", lastname="' + lastname + '", email="' + email + '", password="' + pwd + '", role_id="' + role + '" WHERE id ="' + id + '"'
    cur.execute(requete)
    cur.commit()


def deleteUser(cur, id):
    requete = 'DELETE FROM user WHERE id ="' + id + '"'
    cur.execute(requete)
    cur.commit()


def gen(camera):
    while True:
        frame = camera.get_frame_hand()
        yield (b'--frame\r\n'
            b'Content - Type: image/jpeg\r\n\r\n' + frame
            + b'\r\n\r\n')


# The route
@app.route('/cam/', methods=['GET', 'POST'])
def cam():
    try:
        return render_template('cam.html')

    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print("Unexpected {err=}, {type(err)=}")
        raise

    msg = ''
    return render_template('login.html', msg='')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/deconnection')
def deconnection():
    session.clear()
    return render_template('deconnection.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email'].strip()
            pwd = request.form['password'].strip()
            pwd = hashlib.md5(pwd.encode()).hexdigest()
            
            admin = Admin()
            res = admin.identification(email, pwd)
            for raw in res:
                print (raw[0], raw[1])
                session['name'] = raw[0]
                session['email'] = raw[1]
                session['role'] = raw[2]
                return redirect(url_for('cam', code=302))

    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print("Unexpected ", err, " : ", type(err))
        raise

    return render_template('login.html')


@app.route('/create_user/', methods=['GET', 'POST'])
def create_user():
    admin = Admin()
    try:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            name = request.form['name'].strip()
            lastname = request.form['lastname'].strip()
            email = request.form['email'].strip()
            pwd = request.form['password'].strip()
            pwd = hashlib.md5(pwd.encode()).hexdigest()
            role = request.form['role']
            
            r = admin.createUser(name, lastname, email, pwd, role)
            print("retour insert : ", r)

            # inscription for user
            if "doneUser" in request.form:
                session['name'] = name
                session['email'] = email
                session['role'] = role
            
                return redirect(url_for('cam', code=302))

            return render_template('list_user.html')
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

    req = admin.getRole()
    return render_template('create_user.html', roles=req)


@app.route('/update_user/', methods=['GET', 'POST'])
def update_user():
    cur = connector()
    try:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            id = request.form['id'].strip()
            name = request.form['name'].strip()
            lastname = request.form['lastname'].strip()
            email = request.form['email'].strip()
            pwd = request.form['password'].strip()
            pwd = hashlib.md5(pwd.encode()).hexdigest()
            print("mot de passe :", pwd)
            role = request.form['role']
            print("email :", email)

            # connexion à la BDD mySql

            print("#### update")
            updateUser(cur, id, name, lastname, email, pwd, role)
            # Select all info the movies
            # titlesdb = get_movie_titles(connect)
            msg = ''
            return render_template('modification_user.html', msg='')

    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return render_template('create_user.html', roles=cur.fetchall())


@app.route('/delete_user/', methods=['GET', 'POST'])
def delete_user():
    cur = connector()
    try:
        if request.method == 'POST' and 'id' in request.form:
            id = request.form['id'].strip()

            print("#### delete")
            deleteUser(cur, id)
            # Select all info the movies
            # titlesdb = get_movie_titles(connect)
            msg = ''
            return render_template('modification_user.html', msg='')

    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
    raise


@app.route('/list_user/', methods=['GET', 'POST'])
def list_user():
    admin = Admin()
    return render_template('list_user.html', users=admin.selectUser())


@app.route('/monotoring/', methods=['GET', 'POST'])
def monotoring():
    return render_template('monotoring.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return render_template("index.html")

    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    # unittest.main()
    app.run(host='0.0.0.0')
