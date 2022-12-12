from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    
    password = PasswordField(validators=[InputRequired(), 
        Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")

class TweetsForm(FlaskForm):
	worktweets = StringField("Work Tweet Handles", validators=[InputRequired()]
        ,render_kw={"placeholder":"Work tweet Handles"})
	personaltweets = StringField("Personal Tweet Handles", validators=[InputRequired()]
        ,render_kw={"placeholder":"Personal tweet Handles"})
	submit = SubmitField("Submit")