from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    bedrooms = StringField('Number of Bedrooms', validators=[InputRequired()])
    bathrooms = StringField('Number of Bathrooms', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    type = SelectField('Type', choices=[('House', 'House'), ('Apartment', 'Apartment')])
    description = TextAreaField('Description', validators=[InputRequired()])
    photo = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg', 'Images only!'])])
