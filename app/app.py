# from cgitb import html
# from numpy import imag
import mysql.connector  # pip install mysql-connector-python
# import pickle
import requests
import os
from werkzeug.utils import secure_filename

from camera import VideoCamera
from model.admin import Admin
from model.user import User
import hashlib  # MD5
from flask import Flask, render_template, redirect, request, session, Response, url_for
from flask_session import Session
import flask_monitoringdashboard as dashboard

app = Flask(__name__)

# monotoring
dashboard.config.init_from(file='config.cfg')  # In order to configure the Dashboard with a configuration-file,
dashboard.bind(app) # add monotoring

#session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
s = requests.Session()

#uploads files
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/lessons')
def lessons():
    return render_template('lessons.html', variable='A.jpg')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            render_template('create_user.html',  name=filename)
    return render_template('upload.html')


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
    req = admin.getRole()
    try:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            name = request.form['name']
            lastname = request.form['lastname']
            email = request.form['email']
            pwd = request.form['password']
            role = request.form['role']
            
            
            if "doneUser" in request.form:
                # form completed by user
                u = User()
                r = u.createUser(name, lastname, email, pwd, role)

                if r is None:
                #une erreur s est produite
                    return render_template('create_user.html', roles=req,  err=1)

                session['name'] = name
                session['email'] = email
                session['role'] = role
                return redirect(url_for('cam', code=302))
            else:
                r = admin.createUser(name, lastname, email, pwd, role)
                print("message :", r)
                if r == False:
                    #une erreur s est produite
                    return render_template('create_user.html', roles=req, err=1)

                return redirect(url_for('list_user', code=302))
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

    
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
    app.run(host='0.0.0.0')
