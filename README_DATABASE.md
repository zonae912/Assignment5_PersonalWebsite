# Flask Portfolio with Database Integration

## 🎉 What's New - Database Features

Your Flask portfolio now includes a complete database integration with the following features:

### ✅ Completed Features:

1. **Data Access Layer (DAL.py)**
   - Complete SQLite database management
   - CRUD operations for projects
   - Clean separation of concerns
   - Type hints and documentation

2. **Projects Database (projects.db)**
   - SQLite database with `projects` table
   - Columns: id, title, description, image_filename, category, technologies, project_url, duration, role, created_date
   - Automatically created on first run

3. **Dynamic Projects Page**
   - Displays all projects from database in an HTML table
   - Shows: Image thumbnails, Title, Description, Category, Technologies, Duration, and Links
   - Responsive design
   - Empty state when no projects exist

4. **Add Project Form**
   - Form to add new projects at `/add-project`
   - Validates required fields (title, description, image_filename)
   - Optional fields for detailed project information
   - Instant visibility - projects appear immediately on the projects page

5. **Sample Data**
   - Pre-loaded with 2 sample projects (Lovi.AI and Mingle Beyond)
   - Can be cleared and replaced with your own projects

## 🚀 How to Use

### 1. Start the Application

```powershell
cd "c:\Users\Family\Downloads\MSIS Core\AiDD\Assignment6_PersonalWebsite - Flask"
python app.py
```

Visit: `http://localhost:5000`

### 2. View Projects

Navigate to **Projects** page to see all projects from the database displayed in a table format.

### 3. Add a New Project

#### Step 1: Prepare Your Image
1. Place your project image in the `static/images/` folder
2. Supported formats: JPG, PNG, GIF
3. Example: `static/images/my-awesome-project.png`

#### Step 2: Add Project via Form
1. Click **"Add New Project"** button on the Projects page
2. Or navigate to: `http://localhost:5000/add-project`
3. Fill out the form:
   - **Title** * (Required): Your project name
   - **Description** * (Required): Detailed description
   - **Image Filename** * (Required): Just the filename (e.g., `my-awesome-project.png`)
   - **Category** (Optional): e.g., "Web Development"
   - **Technologies** (Optional): e.g., "Python, Flask, SQLite"
   - **Duration** (Optional): e.g., "Jan 2024 - Mar 2024"
   - **Role** (Optional): e.g., "Lead Developer"
   - **Project URL** (Optional): Link to live site or GitHub

4. Click **"Add Project"**
5. You'll be redirected to the Projects page where your new project will be visible immediately!

## 📁 File Structure

```
Assignment6_PersonalWebsite - Flask/
├── app.py                      # Flask routes (includes add_project route)
├── DAL.py                      # Data Access Layer for database operations
├── projects.db                 # SQLite database (created automatically)
├── requirements.txt            # Python dependencies
├── templates/
│   ├── base.html              # Base template
│   ├── projects.html          # Dynamic projects page with table
│   ├── add_project.html       # Form to add new projects
│   └── ... (other templates)
├── static/
│   ├── css/
│   │   ├── styles.css         # Main styles
│   │   └── projects-styles.css # Projects table styles
│   └── images/                # Project images go here!
│       ├── LoviSC.png
│       ├── mingleSC.png
│       └── (your images here)
└── README_DATABASE.md          # This file
```

## 💾 Database Schema

### Projects Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| title | TEXT | Project title (required) |
| description | TEXT | Project description (required) |
| image_filename | TEXT | Image file name (required) |
| category | TEXT | Project category (optional) |
| technologies | TEXT | Technologies used (optional) |
| project_url | TEXT | Live project URL (optional) |
| duration | TEXT | Project duration (optional) |
| role | TEXT | Your role (optional) |
| created_date | TIMESTAMP | Auto-generated timestamp |

## 🛠️ DAL.py Methods

### Available Methods:

```python
# Initialize database
dal = DAL()

# Add a project
project_id = dal.add_project(
    title="My Project",
    description="Description here",
    image_filename="project.png",
    category="Web Development",  # optional
    technologies="Python, Flask",  # optional
    project_url="https://example.com",  # optional
    duration="Jan 2024",  # optional
    role="Developer"  # optional
)

# Get all projects
projects = dal.get_all_projects()

# Get specific project
project = dal.get_project_by_id(1)

# Update project
dal.update_project(1, title="Updated Title")

# Delete project
dal.delete_project(1)

# Seed sample data
dal.seed_sample_data()
```

## 🎨 Customization

### Adding Custom Fields

To add more fields to the projects table:

1. **Update DAL.py** - Add column in `init_database()`:
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        ...
        your_new_field TEXT,
        ...
    )
''')
```

2. **Update add_project method** in DAL.py

3. **Update the form** in `templates/add_project.html`

4. **Update the display** in `templates/projects.html`

### Changing Table Styles

Edit `static/css/projects-styles.css` to customize:
- Table colors
- Column widths
- Thumbnail sizes
- Responsive behavior

## 🔄 Managing Data

### Clear All Projects

```python
# In Python terminal or script
from DAL import DAL

dal = DAL()

# Get all projects and delete them
projects = dal.get_all_projects()
for project in projects:
    dal.delete_project(project['id'])
```

### Re-seed Sample Data

```powershell
python DAL.py
```

### Backup Database

```powershell
Copy-Item "projects.db" "projects_backup.db"
```

### Reset Database

```powershell
Remove-Item "projects.db" -Force
python DAL.py
```

## ✨ Example: Adding Your First Project

1. **Save your project screenshot** as `my-portfolio-site.png` in `static/images/`

2. **Navigate to Add Project form**: `http://localhost:5000/add-project`

3. **Fill out the form**:
   - Title: `Personal Portfolio Website`
   - Description: `A responsive portfolio website built with Flask, featuring dynamic content management and modern design.`
   - Image Filename: `my-portfolio-site.png`
   - Category: `Web Development`
   - Technologies: `Python, Flask, SQLite, HTML5, CSS3`
   - Duration: `October 2025`
   - Role: `Full Stack Developer`
   - Project URL: `http://localhost:5000`

4. **Click Add Project** - Done! Your project is now visible on the Projects page.

## 🐛 Troubleshooting

### Database Not Found
- The database is created automatically when you run `python app.py`
- If missing, run: `python DAL.py`

### Image Not Displaying
- Verify image is in `static/images/` folder
- Check filename matches exactly (case-sensitive)
- Supported formats: JPG, JPEG, PNG, GIF

### Form Submission Error
- Ensure title, description, and image_filename are filled out
- Check browser console for JavaScript errors
- Check terminal for Flask errors

### No Projects Showing
- Run `python DAL.py` to seed sample data
- Check database: `sqlite3 projects.db` then `SELECT * FROM projects;`

## 📚 Next Steps

Consider adding these features:

- **Edit Projects**: Add an edit button and form
- **Delete Projects**: Add delete functionality with confirmation
- **Image Upload**: Allow direct image upload instead of manual file placement
- **Project Categories**: Filter projects by category
- **Search**: Add search functionality
- **Pagination**: For when you have many projects
- **Admin Panel**: Secure admin area for management

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)

---

**Created**: October 2025  
**Version**: 1.0  
**Author**: AI Development Assistant

Happy coding! 🚀
