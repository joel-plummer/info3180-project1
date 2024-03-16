"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from app.models import Property
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.forms import PropertyForm
from werkzeug.utils import secure_filename

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    property = PropertyForm()
    # Validate file upload on submit
    if property.validate_on_submit() and request.method == 'POST':
        # Get file data and save to your uploads folder
        title = property.title.data
        bedrooms = property.bedrooms.data
        bathrooms = property.bathrooms.data
        location = property.location.data
        price = property.price.data
        type = property.type.data
        description = property.description.data
        photo = property.photo.data
        filename = secure_filename(photo.filename)
        property = Property(title, bedrooms, bathrooms, location, price, type, description, filename)
        db.session.add(property)
        db.session.commit()
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Property successfully added', 'success')
        return redirect(url_for('properties')) # Update this to redirect the user to a route that displays all uploaded image files
    flash_errors(property)
    return render_template('create.html', form=property) # Update this to redirect the user 

@app.route('/properties')
def properties():
    properties = Property.query.all()
    print(properties)
    """Render the website's properties page."""
    return render_template('properties.html', properties=properties)



@app.route('/properties/<propertyid>')
def get_property(propertyid):
    property = Property.query.filter_by(id=propertyid).first()
    """Render the website's property page."""
    return render_template('property.html',property=property)

@app.route('/uploads/<filename>')
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)    
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Joel Plummer")


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
