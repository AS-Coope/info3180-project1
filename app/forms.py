from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[InputRequired()])
    numOfBedrooms = StringField('Number of Bedrooms', validators=[InputRequired()])
    numOfBathrooms = StringField('Number of Bathrooms', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price = StringField('Price of property',validators=[InputRequired()])
    type = SelectField('Type of property', choices=[('Apartment'), ('House')], validate_choice=True)
    description = TextAreaField('Describe the property (200 characters max)')
    property_photo = FileField(
        'Property Photo', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png'], 'Images only!')
        ]
    )