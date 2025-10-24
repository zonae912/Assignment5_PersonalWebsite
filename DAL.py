"""
Data Access Layer (DAL) for Flask Portfolio Website
Handles all database interactions for the projects database
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
import os

class DAL:
    """Data Access Layer for managing database operations"""
    
    def __init__(self, db_name: str = 'projects.db'):
        """
        Initialize the DAL with database name
        
        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Create and return a database connection
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        conn = sqlite3.Connection(self.db_name)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_filename TEXT NOT NULL,
                category TEXT,
                technologies TEXT,
                project_url TEXT,
                duration TEXT,
                role TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database '{self.db_name}' initialized successfully.")
    
    def add_project(self, title: str, description: str, image_filename: str, 
                   category: str = None, technologies: str = None, 
                   project_url: str = None, duration: str = None, 
                   role: str = None) -> int:
        """
        Add a new project to the database
        
        Args:
            title: Project title
            description: Project description
            image_filename: Name of the image file in static/images folder
            category: Project category (optional)
            technologies: Technologies used (optional)
            project_url: URL to live project (optional)
            duration: Project duration (optional)
            role: Your role in the project (optional)
            
        Returns:
            int: ID of the newly created project
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (title, description, image_filename, category, 
                                technologies, project_url, duration, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, image_filename, category, technologies, 
              project_url, duration, role))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return project_id
    
    def get_all_projects(self) -> List[Dict]:
        """
        Retrieve all projects from the database
        
        Returns:
            List[Dict]: List of all projects as dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, image_filename, category, 
                   technologies, project_url, duration, role, created_date
            FROM projects
            ORDER BY created_date DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows to list of dictionaries
        projects = []
        for row in rows:
            projects.append({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'image_filename': row['image_filename'],
                'category': row['category'],
                'technologies': row['technologies'],
                'project_url': row['project_url'],
                'duration': row['duration'],
                'role': row['role'],
                'created_date': row['created_date']
            })
        
        return projects
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict]:
        """
        Get a specific project by ID
        
        Args:
            project_id: ID of the project to retrieve
            
        Returns:
            Optional[Dict]: Project data as dictionary or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, image_filename, category, 
                   technologies, project_url, duration, role, created_date
            FROM projects
            WHERE id = ?
        ''', (project_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'image_filename': row['image_filename'],
                'category': row['category'],
                'technologies': row['technologies'],
                'project_url': row['project_url'],
                'duration': row['duration'],
                'role': row['role'],
                'created_date': row['created_date']
            }
        return None
    
    def update_project(self, project_id: int, title: str = None, 
                      description: str = None, image_filename: str = None,
                      category: str = None, technologies: str = None,
                      project_url: str = None, duration: str = None,
                      role: str = None) -> bool:
        """
        Update an existing project
        
        Args:
            project_id: ID of the project to update
            Other args: Fields to update (only provided fields will be updated)
            
        Returns:
            bool: True if update successful, False otherwise
        """
        # Build dynamic UPDATE query based on provided fields
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if image_filename is not None:
            updates.append("image_filename = ?")
            params.append(image_filename)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if technologies is not None:
            updates.append("technologies = ?")
            params.append(technologies)
        if project_url is not None:
            updates.append("project_url = ?")
            params.append(project_url)
        if duration is not None:
            updates.append("duration = ?")
            params.append(duration)
        if role is not None:
            updates.append("role = ?")
            params.append(role)
        
        if not updates:
            return False
        
        params.append(project_id)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = f"UPDATE projects SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project from the database
        
        Args:
            project_id: ID of the project to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def seed_sample_data(self):
        """Add sample projects to the database for testing"""
        sample_projects = [
            {
                'title': 'Lovi.AI - AI Startup Website Design & Development',
                'description': 'Designed and helped develop the complete front-end for Lovi.AI, an innovative artificial intelligence startup based in Madrid, Spain. Led the UI/UX design process from concept to implementation using Figma, creating a modern, user-friendly interface that effectively communicates the company\'s AI solutions while enhancing user engagement and conversion rates.',
                'image_filename': 'LoviSC.png',
                'category': 'Web Design & Development',
                'technologies': 'Figma, UI/UX Design, HTML5, CSS3, Responsive Design',
                'project_url': 'https://lovi.ai/',
                'duration': 'June 2023',
                'role': 'Lead Designer & Front-End Developer'
            },
            {
                'title': 'Mingle Beyond - Social Platform for Recent Graduates',
                'description': 'Mingle Beyond is a comprehensive web platform designed to help recent college graduates stay connected and supported during the major transition from college to professional life. The platform addresses feelings of isolation and uncertainty by providing a space where users can meet new people, explore shared interests, and build genuine connections within a supportive community.',
                'image_filename': 'mingleSC.png',
                'category': 'Senior Capstone',
                'technologies': 'PHP, MySQL, Google Maps API, Google Login, HTML5, CSS3, JavaScript',
                'project_url': 'https://zion-zion.webapps.iu.edu/info-capstone-2025/mingle-beyond#project',
                'duration': 'Fall 2024 - Spring 2025',
                'role': 'Team Member (Team 27)'
            }
        ]
        
        for project in sample_projects:
            self.add_project(**project)
        
        print(f"Added {len(sample_projects)} sample projects to the database.")


# Convenience function to get DAL instance
def get_dal() -> DAL:
    """
    Get a DAL instance
    
    Returns:
        DAL: Data Access Layer instance
    """
    return DAL()


if __name__ == '__main__':
    # Test the DAL
    dal = DAL()
    print("Database initialized.")
    
    # Seed with sample data
    dal.seed_sample_data()
    
    # Display all projects
    projects = dal.get_all_projects()
    print(f"\nTotal projects: {len(projects)}")
    for project in projects:
        print(f"- {project['title']}")
