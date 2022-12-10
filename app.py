from flask import Flask, flash, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import tweetscrape

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'renergy48'
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

current_logged_in_user = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User{}>'.format(self.username)
    
    def get_username(self):
        return self.username

    def __str__(self) -> str:
        return self.username

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Register")

    # def validate_username(self, username):
    #     existing_user_username = User.query.filter_by(
    #         username=username.data).first()
    #     if existing_user_username:
    #         flash("User already exists!")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")

# @app.route('/')
# def home():
#     return render_template('base.html')

@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # exists = db.session.query(User.id).filter_by(username=form.username.data).first() is not None
        # if exists:
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                flash("Login successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password! Try Again!")
        else:
            flash("User does not exist")
    return render_template('login.html',form=form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))
 
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    # form.validate_username(form.username)
    if db.session.query(User.id).filter_by(username=form.username.data).first() is not None:
        flash("User already exists!")
    elif form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    data = tweetscrape.randomtweet('thequote',9)
    return render_template('dashboard.html',data=data)


# @app.route('/test')
# def test():
#     sites = [1,2,2,3,4]
#     return render_template('home.html',sites=sites)
if __name__ == '__main__':
    app.run(debug=True )