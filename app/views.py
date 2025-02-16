"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, flash, request, redirect, url_for, send_from_directory
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

@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    #Instantiate form class
    property = PropertyForm()
    #Validate file upon submission
    if property.validate_on_submit():
        prop_title = property.title.data
        prop_numOfBed = property.numOfBedrooms.data
        prop_numOfBath = property.numOfBathrooms.data
        prop_location = property.location.data
        prop_price = property.price.data
        prop_type = property.type.data
        prop_desc = property.description.data
        prop_photo = property.property_photo.data
        prop_filename = secure_filename(prop_photo.filename)
    
        prop_photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], prop_filename
        ))
        
        prop = Property(prop_title, prop_numOfBed, prop_numOfBath, 
                        prop_location, prop_price, prop_type, prop_desc, prop_filename)
        
        db.session.add(prop)
        db.session.commit()

        flash('Property was successfully added!')
        return redirect(url_for('properties'))
    return render_template('create_property.html', form=property)

@app.route('/properties')
def properties():
    # get all the entries in the property database and store them in a list
    # for each property, grab the name of the file then concatenate it with the uploads folder name to get file path
    all_properties = db.session.execute(db.select(Property)).scalars()
    return render_template('properties.html', props=all_properties)

@app.route('/properties/<propertyid>')
def property(propertyid):
    indiv_prop = db.session.execute(db.select(Property).filter_by(id=propertyid)).scalar()
    return render_template('property.html', property=indiv_prop)

@app.route('/upload/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

def get_uploaded_images():
    rootdir = os.getcwd()
    filenames = []
    #print(rootdir)
    for subdir, dirs, files in os.walk(rootdir + app.config['UPLOAD_FOLDER']):
        for file in files:
            filenames.append(file)

    return filenames
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
