# Evan Zona - Personal Portfolio Website (Flask Version)

A Flask-based personal portfolio website showcasing professional skills, interests, and accomplishments. Converted from static HTML to a dynamic Flask application with server-side form processing.

## 🌟 Features

### Design & User Experience
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Clean UI**: Professional design with gradient backgrounds and smooth styling
- **Flask Templates**: Uses Jinja2 templating for maintainable code
- **Server-side Form Processing**: Contact form with validation and flash messages
- **Mobile Menu**: Responsive navigation for smaller screens

### Pages
- **Home**: Professional introduction with call-to-action buttons
- **About**: Personal introduction with professional statistics and values
- **Resume**: Embedded PDF viewer for resume
- **Projects**: Showcase of professional and academic work
- **Contact**: Working contact form with server-side validation
- **Thank You**: Confirmation page after form submission

### Technical Features
- **Flask Framework**: Python web framework for routing and server logic
- **Jinja2 Templates**: Template inheritance for DRY code
- **Form Validation**: Both client-side and server-side validation
- **Flash Messages**: User feedback for form submissions
- **Static File Serving**: Proper handling of CSS, images, and other assets
- **RESTful Routes**: Clean URL structure

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**
   ```bash
   cd "Assignment6_PersonalWebsite - Flask"
   ```

2. **Create a virtual environment (recommended)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the Flask application**
   ```powershell
   python app.py
   ```

5. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
Assignment6_PersonalWebsite - Flask/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/                  # Jinja2 templates
│   ├── base.html              # Base template with nav/footer
│   ├── index.html             # Home page
│   ├── about.html             # About page
│   ├── resume.html            # Resume page
│   ├── projects.html          # Projects page
│   ├── contact.html           # Contact form page
│   └── thankyou.html          # Thank you page
├── static/                     # Static files
│   ├── css/
│   │   └── styles.css         # All CSS styles
│   └── images/                # Image assets
└── prompts/                    # Development notes
    └── dev_notes.md
```

## 🎨 Customization

### Update Content
All content is in the template files in the `templates/` directory. Update:
- Personal information in `templates/index.html`
- Bio and background in `templates/about.html`
- Project details in `templates/projects.html`
- Contact information in `templates/contact.html`

### Update Styles
All CSS is in `static/css/styles.css`. The website uses CSS custom properties for easy theming:

```css
:root {
    --primary-color: #4f46e5;    /* Main brand color */
    --secondary-color: #06b6d4;   /* Accent color */
    --accent-color: #f59e0b;      /* Highlight color */
    /* ... other variables */
}
```

### Update Secret Key
**Important**: Change the secret key in `app.py` before deploying to production:

```python
app.secret_key = 'your-secret-key-here-change-in-production'
```

Generate a secure secret key:
```python
import secrets
secrets.token_hex(16)
```

### Add Database Support
To save contact form submissions to a database:

1. Install Flask-SQLAlchemy:
   ```powershell
   pip install flask-sqlalchemy
   ```

2. Add database configuration to `app.py`:
   ```python
   from flask_sqlalchemy import SQLAlchemy
   
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
   db = SQLAlchemy(app)
   
   class Contact(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       first_name = db.Column(db.String(100))
       last_name = db.Column(db.String(100))
       email = db.Column(db.String(120))
       # Add other fields
   ```

## 📱 Routes

- `/` - Home page
- `/about` - About Me page
- `/resume` - Resume page
- `/projects` - Projects showcase
- `/contact` - Contact form (GET and POST)
- `/thankyou` - Thank you confirmation

## ⚡ Development Features

### Debug Mode
The application runs in debug mode by default (see `app.py`):
```python
app.run(debug=True, port=5000)
```

**Note**: Set `debug=False` in production!

### Form Validation
The contact form includes:
- Required field validation
- Email format validation
- Password strength requirements
- Password confirmation matching
- Server-side validation with flash messages

### Flash Messages
User feedback is provided through Flask's flash message system:
- Success messages (green)
- Error messages (red)
- Automatically styled and positioned

## 🚀 Deployment

### Preparation for Production

1. **Update secret key**
   ```python
   app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')
   ```

2. **Turn off debug mode**
   ```python
   app.run(debug=False)
   ```

3. **Use a production server**
   Install Gunicorn:
   ```powershell
   pip install gunicorn
   ```
   
   Run with Gunicorn:
   ```bash
   gunicorn app:app
   ```

### Deploy to Various Platforms

**Heroku:**
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   heroku create
   git push heroku main
   ```

**PythonAnywhere / Render / Railway:**
Follow their Flask deployment guides, making sure to:
- Install dependencies from `requirements.txt`
- Set environment variables for SECRET_KEY
- Configure the WSGI application

## 🔧 Troubleshooting

### CSS not loading
- Check that `styles.css` is in `static/css/` directory
- Verify Flask is serving static files correctly
- Clear browser cache

### Images not displaying
- Ensure images are in `static/images/` directory
- Check file names match exactly (case-sensitive)
- Use `url_for('static', filename='images/filename.ext')`

### Form not submitting
- Check that form action points to `{{ url_for('contact') }}`
- Verify method is POST
- Check browser console for JavaScript errors

## 📝 License

© 2025 Evan Zona. All rights reserved.

## 🤝 Contributing

This is a personal portfolio project. Feel free to fork and adapt for your own use!

## 📧 Contact

- **Email**: evanbzona@gmail.com
- **LinkedIn**: [linkedin.com/in/evan-zona](https://linkedin.com/in/evan-zona/)
- **GitHub**: [github.com/evanzona](https://github.com/evanzona)
