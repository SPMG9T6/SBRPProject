import unittest
import json
from flask import url_for
from app import app, db

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

    def test_database(self):
        tester = app.test_client(self)
        response = tester.get('/database', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Create Database' in response.data)

    def test_render_template(self):
        tester = app.test_client(self)
        response = tester.get('/render_template', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Hello, World!' in response.data)

    def test_jsonify(self):
        tester = app.test_client(self)
        response = tester.get('/jsonify', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Hello, World!'})

    def test_request(self):
        tester = app.test_client(self)
        response = tester.post('/request', data={'name': 'John'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Hello, John!'})

    def test_redirect(self):
        tester = app.test_client(self)
        response = tester.get('/redirect', content_type='html/text')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/')

    def test_url_for(self):
        with app.test_request_context():
            assert url_for('index') == '/'
            assert url_for('database') == '/database'
            assert url_for('render_template') == '/render_template'
            assert url_for('jsonify') == '/jsonify'
            assert url_for('request') == '/request'
            assert url_for('redirect') == '/redirect'


# Staff View Testing - Happy Path

    def test_view_employee(self):
        tester = app.test_client(self)
        response = tester.get('/view_employee', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'View Employee' in response.data)   

# Staff View Testing - Negative Path

def test_view_non_existent_employee(self):
    tester = app.test_client(self)
    response = tester.get('/view_employee/9999', content_type='html/text')
    self.assertEqual(response.status_code, 404)


# Staff View Testing - Boundary Path 

def test_view_employee_boundary(self):
    tester = app.test_client(self)

    # Test with smallest possible employee ID (assuming it's 1)
    response = tester.get('/view_employee/1', content_type='html/text')
    self.assertEqual(response.status_code, 200)

    # Test with largest possible employee ID (assuming it's 10000)
    response = tester.get('/view_employee/10000', content_type='html/text')
    self.assertEqual(response.status_code, 200)


# Staff Browse Testing - Happy Path

    def test_browse_employee(self):
        tester = app.test_client(self)
        response = tester.get('/browse_employee', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Browse Employee' in response.data)




# Staff Filter roles Testing - Happy Path

    def test_filter_roles(self):
        tester = app.test_client(self)
        response = tester.get('/filter_roles', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Filter Roles' in response.data)

# Staff Filter roles Testing - Negative Path
        def test_filter_roles_non_existent(self):
            tester = app.test_client(self)
            response = tester.get('/filter_roles?role=NonExistentRole', content_type='html/text')
            self.assertEqual(response.status_code, 404)

# Staff Filter roles Testing - Boundary Path
def test_filter_roles_boundary(self):
    tester = app.test_client(self)

    # Test with smallest possible role ID (assuming it's 1)
    response = tester.get('/filter_roles?role_id=1', content_type='html/text')
    self.assertEqual(response.status_code, 200)

    # Test with largest possible role ID (assuming it's 10000)
    response = tester.get('/filter_roles?role_id=10000', content_type='html/text')
    self.assertEqual(response.status_code, 200)


# Staff Filter department Testing - Happy Path

    def test_filter_department(self):
        tester = app.test_client(self)
        response = tester.get('/filter_department', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Filter Department' in response.data)

# Staff Filter department Testing - Negative Path
        def test_filter_department_non_existent(self):
            tester = app.test_client(self)
            response = tester.get('/filter_department?department=NonExistentDepartment', content_type='html/text')
            self.assertEqual(response.status_code, 404)

# Staff Filter department Testing - Boundary Path
def test_filter_department_boundary(self):
    tester = app.test_client(self)

    # Test with smallest possible department ID (assuming it's 1)
    response = tester.get('/filter_department?department_id=1', content_type='html/text')
    self.assertEqual(response.status_code, 200)

    # Test with largest possible department ID (assuming it's 10000)
    response = tester.get('/filter_department?department_id=10000', content_type='html/text')
    self.assertEqual(response.status_code, 200)


# Staff Apply Testing - Happy Path

    def test_apply(self):
        tester = app.test_client(self)
        response = tester.get('/apply', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Apply' in response.data)

# Staff Apply Testing - Negative Path
def test_apply_non_existent(self):
    tester = app.test_client(self)
    response = tester.get('/apply/9999', content_type='html/text')
    self.assertEqual(response.status_code, 404)


 # Staff Apply Testing - Boundary Path
    def test_apply_boundary(self):
        tester = app.test_client(self)

        # Test with smallest possible application ID (assuming it's 1)
        response = tester.get('/apply/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Test with largest possible application ID (assuming it's 10000)
        response = tester.get('/apply/10000', content_type='html/text')
        self.assertEqual(response.status_code, 200)


# Hr View Tests - Happy Path

    def test_view_hr(self):
        tester = app.test_client(self)
        response = tester.get('/view_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'View HR' in response.data)

# HR View Tests - Negative Path
def test_view_hr_non_existent(self):
    tester = app.test_client(self)
    response = tester.get('/view_hr/9999', content_type='html/text')
    self.assertEqual(response.status_code, 404)

    # HR View Tests - Boundary Path
    def test_view_hr_boundary(self):
        tester = app.test_client(self)

        # Test with smallest possible HR ID (assuming it's 1)
        response = tester.get('/view_hr/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Test with largest possible HR ID (assuming it's 10000)
        response = tester.get('/view_hr/10000', content_type='html/text')
        self.assertEqual(response.status_code, 200)



# HR CRU TESTS - Create, Read, Update

# HR Create Tests - Happy Path
    def test_create_hr(self):
        tester = app.test_client(self)
        response = tester.get('/create_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Create HR' in response.data)


# HR Create Tests - Negative Path (Role Already Created)
    def test_create_hr(self):
        tester = app.test_client(self)
        response = tester.get('/create_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Already Created' in response.data)

# HR Create Tests - Bounrdary Path 
def test_create_hr_boundary(self):
    tester = app.test_client(self)

    # Test with smallest possible HR ID (assuming it's 1)
    response = tester.get('/create_hr/1', content_type='html/text')
    self.assertEqual(response.status_code, 200)

    # Test with largest possible HR ID (assuming it's 10000)
    response = tester.get('/create_hr/10000', content_type='html/text')
    self.assertEqual(response.status_code, 200)


# HR View Tests - Negative Path
def test_view_hr_non_existent(self):
    tester = app.test_client(self)
    response = tester.get('/view_hr/9999', content_type='html/text')
    self.assertEqual(response.status_code, 404)

     # HR View Tests - Boundary Path
    def test_view_hr_boundary(self):
        tester = app.test_client(self)

        # Test with smallest possible HR ID (assuming it's 1)
        response = tester.get('/view_hr/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Test with largest possible HR ID (assuming it's 10000)
        response = tester.get('/view_hr/10000', content_type='html/text')
        self.assertEqual(response.status_code, 200)

# HR View Tests - Boundary Path
def test_view_hr_boundary(self):
    tester = app.test_client(self)

    # Test with smallest possible HR ID (assuming it's 1)
    response = tester.get('/view_hr/1', content_type='html/text')
    self.assertEqual(response.status_code, 200)

    # Test with largest possible HR ID (assuming it's 10000)
    response = tester.get('/view_hr/10000', content_type='html/text')
    self.assertEqual(response.status_code, 200)


# HR Read Tests - Happy Path

    def test_read_hr(self):

        tester = app.test_client(self)
        response = tester.get('/read_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Read HR' in response.data)

# HR Read Tests - Negative Path (Role Already Created)

    def test_read_hr(self):
            
            tester = app.test_client(self)
            response = tester.get('/read_hr', content_type='html/text')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Role Listing Already Created' in response.data)

# HR Read Tests - Boundary Path
def test_read_hr_boundary(self):
    tester = app.test_client(self)

    # Test with smallest possible HR ID (assuming it's 1)
    response = tester.get('/read_hr/1', content_type='html/text')
    self.assertEqual(response.status_code, 200)

    # Test with largest possible HR ID (assuming it's 10000)
    response = tester.get('/read_hr/10000', content_type='html/text')
    self.assertEqual(response.status_code, 200)


# HR Update Tests - Happy Path

    def test_update_hr(self):

        tester = app.test_client(self)
        response = tester.get('/add_role_listing/create', content_type='html/text')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Role Listing Created Successfully' in response.data)

# HR Update Tests - Negative Path 

    def test_update_hr(self):
                
                tester = app.test_client(self)
                response = tester.get('/add_role_listing/create', content_type='html/text')
                self.assertEqual(response.status_code, 200)
                self.assertTrue(b'Role Listing Already Created' in response.data)

# HR Update Tests - Boundary Path

def test_update_hr_boundary(self):
    tester = app.test_client(self)

    # Test with smallest possible HR ID (assuming it's 1)
    response = tester.get('/add_role_listing/create/1', content_type='html/text')
    self.assertEqual(response.status_code, 200)

    # Test with largest possible HR ID (assuming it's 10000)
    response = tester.get('/add_role_listing/create/10000', content_type='html/text')
    self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

