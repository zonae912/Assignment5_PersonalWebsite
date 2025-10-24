from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from DAL import DAL

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Change this in production

# Initialize Database Access Layer
dal = DAL()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/projects')
def projects():
    """Display all projects from the database"""
    all_projects = dal.get_all_projects()
    return render_template('projects.html', projects=all_projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        newsletter = request.form.get('newsletter')
        
        # Basic validation
        errors = []
        
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html')
        
        # In a real application, you would:
        # - Save the contact information to a database
        # - Send an email notification
        # - Hash the password before storing
        
        # For now, just redirect to thank you page
        flash(f'Thank you, {first_name}! Your message has been received.', 'success')
        return redirect(url_for('thankyou'))
    
    return render_template('contact.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/add-project', methods=['GET', 'POST'])
def add_project():
    """Form to add new projects to the database"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        image_filename = request.form.get('image_filename')
        category = request.form.get('category')
        technologies = request.form.get('technologies')
        project_url = request.form.get('project_url')
        duration = request.form.get('duration')
        role = request.form.get('role')
        
        # Validation
        errors = []
        if not title:
            errors.append('Project title is required')
        if not description:
            errors.append('Project description is required')
        if not image_filename:
            errors.append('Image filename is required')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add_project.html')
        
        # Add project to database
        try:
            project_id = dal.add_project(
                title=title,
                description=description,
                image_filename=image_filename,
                category=category,
                technologies=technologies,
                project_url=project_url,
                duration=duration,
                role=role
            )
            flash(f'Project "{title}" added successfully!', 'success')
            return redirect(url_for('projects'))
        except Exception as e:
            flash(f'Error adding project: {str(e)}', 'error')
            return render_template('add_project.html')
    
    return render_template('add_project.html')

if __name__ == '__main__':
    # Use 0.0.0.0 to make the app accessible from outside the container
    app.run(host='0.0.0.0', debug=False, port=5000)
