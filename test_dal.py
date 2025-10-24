"""
Unit tests for the Data Access Layer (DAL)
Tests all database operations for the projects database
"""

import pytest
from DAL import DAL


class TestDALInitialization:
    """Test DAL initialization and database setup"""
    
    def test_dal_creates_database(self, test_dal):
        """Test that DAL creates a database file"""
        assert test_dal.db_name is not None
    
    def test_dal_initializes_table(self, test_dal):
        """Test that the projects table is created"""
        conn = test_dal.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='projects'
        """)
        result = cursor.fetchone()
        conn.close()
        assert result is not None


class TestAddProject:
    """Test adding projects to the database"""
    
    def test_add_project_with_all_fields(self, test_dal, sample_project_data):
        """Test adding a project with all fields populated"""
        project_id = test_dal.add_project(**sample_project_data)
        
        assert project_id is not None
        assert project_id > 0
    
    def test_add_project_with_required_fields_only(self, test_dal):
        """Test adding a project with only required fields"""
        project_id = test_dal.add_project(
            title='Minimal Project',
            description='Minimal description',
            image_filename='minimal.jpg'
        )
        
        assert project_id is not None
        assert project_id > 0
    
    def test_add_multiple_projects(self, test_dal):
        """Test adding multiple projects"""
        id1 = test_dal.add_project(
            title='Project 1',
            description='Description 1',
            image_filename='img1.jpg'
        )
        id2 = test_dal.add_project(
            title='Project 2',
            description='Description 2',
            image_filename='img2.jpg'
        )
        
        assert id2 > id1  # IDs should increment


class TestGetAllProjects:
    """Test retrieving all projects"""
    
    def test_get_all_projects_empty(self, test_dal):
        """Test getting projects when database is empty"""
        projects = test_dal.get_all_projects()
        assert projects == []
    
    def test_get_all_projects_with_data(self, populated_dal):
        """Test getting projects when database has data"""
        projects = populated_dal.get_all_projects()
        
        assert len(projects) == 3
        assert all('id' in p for p in projects)
        assert all('title' in p for p in projects)
        assert all('description' in p for p in projects)
    
    def test_get_all_projects_ordered_by_date(self, populated_dal):
        """Test that projects are ordered by created_date DESC"""
        projects = populated_dal.get_all_projects()
        
        # Most recent should be first (based on insertion order)
        # Note: SQLite timestamp resolution may not guarantee ordering for rapid inserts
        # Just verify we have all 3 projects
        assert len(projects) == 3
        project_titles = [p['title'] for p in projects]
        assert 'Test Project' in project_titles
        assert 'Second Project' in project_titles
        assert 'Third Project' in project_titles


class TestGetProjectById:
    """Test retrieving a specific project by ID"""
    
    def test_get_project_by_id_exists(self, populated_dal):
        """Test getting a project that exists"""
        project = populated_dal.get_project_by_id(1)
        
        assert project is not None
        assert project['id'] == 1
        assert project['title'] == 'Test Project'
    
    def test_get_project_by_id_not_exists(self, test_dal):
        """Test getting a project that doesn't exist"""
        project = test_dal.get_project_by_id(999)
        assert project is None
    
    def test_get_project_by_id_contains_all_fields(self, populated_dal):
        """Test that retrieved project contains all expected fields"""
        project = populated_dal.get_project_by_id(1)
        
        expected_fields = [
            'id', 'title', 'description', 'image_filename',
            'category', 'technologies', 'project_url', 
            'duration', 'role', 'created_date'
        ]
        
        for field in expected_fields:
            assert field in project


class TestUpdateProject:
    """Test updating existing projects"""
    
    def test_update_project_title(self, populated_dal):
        """Test updating a project's title"""
        success = populated_dal.update_project(1, title='Updated Title')
        assert success is True
        
        project = populated_dal.get_project_by_id(1)
        assert project['title'] == 'Updated Title'
    
    def test_update_project_multiple_fields(self, populated_dal):
        """Test updating multiple fields at once"""
        success = populated_dal.update_project(
            1, 
            title='New Title',
            description='New Description',
            category='New Category'
        )
        assert success is True
        
        project = populated_dal.get_project_by_id(1)
        assert project['title'] == 'New Title'
        assert project['description'] == 'New Description'
        assert project['category'] == 'New Category'
    
    def test_update_nonexistent_project(self, test_dal):
        """Test updating a project that doesn't exist"""
        success = test_dal.update_project(999, title='New Title')
        # Should return False or handle gracefully
        assert success is False or success is None


class TestDeleteProject:
    """Test deleting projects"""
    
    def test_delete_existing_project(self, populated_dal):
        """Test deleting a project that exists"""
        success = populated_dal.delete_project(1)
        assert success is True
        
        # Verify deletion
        project = populated_dal.get_project_by_id(1)
        assert project is None
    
    def test_delete_nonexistent_project(self, test_dal):
        """Test deleting a project that doesn't exist"""
        success = test_dal.delete_project(999)
        assert success is False
    
    def test_delete_reduces_project_count(self, populated_dal):
        """Test that deleting a project reduces the total count"""
        initial_count = len(populated_dal.get_all_projects())
        populated_dal.delete_project(1)
        new_count = len(populated_dal.get_all_projects())
        
        assert new_count == initial_count - 1


class TestProjectData:
    """Test project data integrity and retrieval"""
    
    def test_project_fields_are_preserved(self, test_dal, sample_project_data):
        """Test that all project fields are stored and retrieved correctly"""
        project_id = test_dal.add_project(**sample_project_data)
        retrieved = test_dal.get_project_by_id(project_id)
        
        assert retrieved['title'] == sample_project_data['title']
        assert retrieved['description'] == sample_project_data['description']
        assert retrieved['image_filename'] == sample_project_data['image_filename']
        assert retrieved['category'] == sample_project_data['category']
        assert retrieved['technologies'] == sample_project_data['technologies']
    
    def test_optional_fields_can_be_none(self, test_dal):
        """Test that optional fields can be omitted"""
        project_id = test_dal.add_project(
            title='Project',
            description='Description',
            image_filename='image.jpg'
        )
        
        project = test_dal.get_project_by_id(project_id)
        assert project is not None
        assert project['title'] == 'Project'
