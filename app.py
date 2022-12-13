from flask import Flask, flash, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
import tweetscrape
from webforms import RegisterForm,LoginForm,TweetsForm

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

class TweetHandles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worktweets = db.Column(db.JSON)
    personaltweets = db.Column(db.JSON)
    connection_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

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
    form = TweetsForm()

    if TweetHandles.query.filter_by(connection_id=current_user.id).first() is None:
        flash("To begin add handles!")
        return redirect(url_for('settings'))

    relevant_data = TweetHandles.query.filter_by(connection_id=current_user.id).first()
    worktweets = relevant_data.worktweets
    personaltweets = relevant_data.personaltweets

    personaltweetcollate = tweetscrape.tweetfeed(personaltweets,'PERSONAL')
    worktweetcollate = tweetscrape.tweetfeed(worktweets,'WORK')

    return render_template('dashboard.html',form=form,
                personaltweetcollate=personaltweetcollate,
                    worktweetcollate=worktweetcollate)


@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    form = TweetsForm()
    if form.validate_on_submit():
        current_id = current_user.id

        if tweetscrape.checkvalidall(form.worktweets.data) == False:
            flash("One of your work tweet handles does not pass the requirements!")
            return redirect(url_for('settings'))
        if tweetscrape.checkvalidall(form.personaltweets.data) == False:
            flash("One of your personal tweet handles does not pass the requirements!")
            return redirect(url_for('settings'))
        
        if TweetHandles.query.filter_by(connection_id=current_user.id).first() is None:
            tweet_data = TweetHandles(worktweets={'WORK':form.worktweets.data},personaltweets={'PERSONAL':form.personaltweets.data},connection_id=current_id)
            db.session.add(tweet_data)
            db.session.commit()
            
        else:
            existing_tweet_data = TweetHandles.query.filter_by(connection_id=current_user.id).first()
            existing_tweet_data.worktweets = {'WORK':form.worktweets.data}
            existing_tweet_data.personaltweets = {'PERSONAL':form.personaltweets.data}
            db.session.add(existing_tweet_data)
            db.session.commit()

        return redirect(url_for('dashboard'))
    return render_template('settings.html',form=form)

