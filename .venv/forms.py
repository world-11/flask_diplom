from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class AthleteForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Add Athlete')

class CompetitionForm(FlaskForm):
    name = StringField('Competition Name', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Add Competition')

class ParticipationForm(FlaskForm):
    athlete = SelectField('Athlete', coerce=int)
    competition = SelectField('Competition', coerce=int)
    submit = SubmitField('Add Participation')