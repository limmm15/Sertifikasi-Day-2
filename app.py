from pymongo import MongoClient
from bson import ObjectId
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app=Flask(__name__)

SECRET_KEY = "ALIM"

@app.route("/")
def index():
    job = list(db.job.find({}))
    return render_template('index.html', job=job)


# Login
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    print(username_receive, pw_hash)
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )

@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    doc = {
        "username": username_receive,  
        "password": password_hash,  
        "profile_name": username_receive,  
    }
    db.users.insert_one(doc)
    return jsonify({"result": "success"})

@app.route("/sign_up/check_dup", methods=["POST"])
def check_dup():
    username_receive = request.form["username_give"]
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({"result": "success", "exists": exists})



#  Admin Panel
@app.route('/tambah',methods=['GET','POST'])
def dashboard():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        job = list(db.job.find({}))
        return render_template('dashboard.html', job=job, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))
    
@app.route('/job',methods=['GET','POST'])
def job():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        job = list(db.job.find({}))
        return render_template('index_copy.html', job=job, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))
   

@app.route('/addjob',methods=['GET','POST'])
def addjob():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        if request.method == 'POST' :
            nama = request.form['nama']
            deskripsi = request.form['deskripsi']
            nama_gambar = request.files['gambar']
            if nama_gambar :
                nama_file_asli = nama_gambar.filename
                nama_file_gambar = nama_file_asli.split('.')[-1]
                file_path = f'static/assets/imgfruit/{nama_file_gambar}'
                nama_gambar.save(file_path)
            else :
                nama_gambar = None

            doc = {
                "username": user_info["username"],
                'nama' : nama,
                'deskripsi' : deskripsi,
                'foto' : nama_file_gambar
            }
            db.job.insert_one(doc)
            return redirect(url_for('dashboard'))
        return render_template('addjob.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))
   

@app.route('/edit/<_id>',methods=['GET','POST'])
def edit(_id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        if request.method == 'POST' :
            nama = request.form['nama']
            deskripsi = request.form['deskripsi']
            nama_gambar = request.files['gambar']
            doc = {
                'nama' : nama,
                'deskripsi' : deskripsi,
            }

            if nama_gambar :
                nama_file_asli = nama_gambar.filename
                nama_file_gambar = nama_file_asli.split('.')[-1]
                file_path = f'static/assets/imgfruit/{nama_file_gambar}'
                nama_gambar.save(file_path)
                doc['foto'] = nama_file_gambar

            db.job.update_one({'_id': ObjectId(_id)}, {'$set': doc})
            return redirect(url_for("job"))

        id = ObjectId(_id)
        data = db.job.find({'_id':id})
        return render_template('editjob.html',data=data,user_info=user_info)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))
    
@app.route('/delete/<_id>',methods=['GET','POST'])
def delete(_id):
    db.job.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('job'))

if __name__ == '__main__':
    app.run("0.0.0.0",port=5000,debug=True)