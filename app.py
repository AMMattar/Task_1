from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50), nullable =False)
    last_name = db.Column(db.String(50), nullable =False)
    email = db.Column(db.String(150), nullable =False)
    password = db.Column(db.Integer)
    client = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    human = db.Column(db.Boolean)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regist/')
def regist():
    return render_template('regist.html')

@app.route('/regist/admin/', methods=["POST", "GET"])
def admin_regist():
    if request.method == "POST":
        admin_first_name = request.form['first_name']
        admin_last_name = request.form['last_name']
        admin_email = request.form['email']
        admin_password = request.form['password']
        new_admin = Task(first_name = admin_first_name,last_name = admin_last_name, email=admin_email, password=admin_password,client=False,admin = True,human=False)  
        try:
            db.session.add(new_admin)
            db.session.commit()
            return redirect('/')
        except:
            return "sorr, there is an error please try again later"
    else:
        return render_template('admin.html')

@app.route('/regist/client/', methods=["POST", "GET"])
def client_regist():
    if request.method == "POST":
        client_first_name = request.form['first_name']
        client_last_name = request.form['last_name']
        client_email = request.form['email']
        client_password = request.form['password']
        new_client = Task(first_name = client_first_name,last_name = client_last_name, email=client_email, password=client_password,client=True,admin =False,human=False)  
        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect('/')
        except:
            return "Sorry! there is an error please try again later"
    else:
        return render_template('client.html')

@app.route('/regist/human/', methods=["POST", "GET"])
def human_regist():
    if request.method == "POST":
        human_first_name = request.form['first_name']
        human_last_name = request.form['last_name']
        human_email = request.form['email']
        human_password = request.form['password']
        new_human = Task(first_name = human_first_name,last_name = human_last_name, email=human_email, password=human_password,client=False,admin = False,human=True)  
        try:
            db.session.add(new_human)
            db.session.commit()
            return redirect('/')
        except:
            return "Sorry! there is an error please try again later"
    else:
        return render_template('labelerHuman.html')

if __name__ == '__main__':
    app.run(debug=True)