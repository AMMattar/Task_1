from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user

app=Flask(__name__)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Task(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50), nullable =False)
    last_name = db.Column(db.String(50), nullable =False)
    email = db.Column(db.String(150), nullable =False, unique=True)
    password = db.Column(db.Integer)
    client = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    human = db.Column(db.Boolean)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return Task.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regist/')
def regist():
    return render_template('regist.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email =request.form['email']
        password =request.form['password']

        user = Task.query.filter_by(email=email, password=password).first()
        if not user:
            flash('please check your login details')
            return redirect('/login/')
    
        login_user(user)
        return redirect('/profile/')
    else:
        return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/profile/')
@login_required
def profile():
    userName = current_user.first_name
    if current_user.admin == 1 or current_user.client == 1:
        return render_template('adminprofile.html')
    return render_template('profile.html', name=userName)

@app.route('/regist/admin/', methods=["POST", "GET"])
def admin_regist():
    if request.method == "POST":
        admin_first_name = request.form['first_name']
        admin_last_name = request.form['last_name']
        admin_email = request.form['email']
        admin_password = request.form['password']
        new_admin = Task(first_name = admin_first_name,last_name = admin_last_name, email=admin_email, password=admin_password,client=False,admin = True,human=False)  
        
        user = Task.query.filter_by(email=admin_email).first()
        if user:
            flash('This Admin e-mail already exists.')
            return redirect('/regist/admin/')
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
        
        user = Task.query.filter_by(email=client_email).first()
        if user:
            flash('Email address already exists.')
            return redirect('/regist/client/')
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
        
        user = Task.query.filter_by(email=human_email).first()
        if user:
            flash('Email address already exists.')
            return redirect('/regist/human/')
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
