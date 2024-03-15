"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import PropertyForm
from werkzeug.utils import secure_filename
from app.models import Property


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create')
def create_property():
    #Instantiate form class
    property = PropertyForm()
    #Validate file upon submission
    if property.validate_on_submit():
        prop_title = property.title.data
        prop_numOfBed = property.numOfBedrooms.data
        prop_numOfBath = property.numOfBathrooms.data
        location = property.location.data
        price = property.price.data
        type = property.type.data
        desc = property.description.data
        prop_photo = property.property_photo.data
        filename = secure_filename(prop_photo.filname)

        prop_photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        
        flash('Property was successfully added!')
        render_template(redirect(url_for('properties'))) 
    return render_template('create_property.html')

@app.route('/properties')
def properties():
    pass

@app.route('/properties/<propertyid>')
def property():
    pass


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
