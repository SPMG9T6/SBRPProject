import unittest
import json
from flask import url_for
import unittest
from app import app, db, Role, Role_Applicants

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                            'root:root' + \
                                            '@localhost:3306/sbrpdb'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_role(self):
        response = self.app.post('/role/create', data=dict(role_name='Test Role', role_desc='This is a test role'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'create successfully', response.data)
        role = Role.query.filter_by(role_name='Test Role').first()
        self.assertIsNotNone(role)
        self.assertEqual(role.role_desc, 'This is a test role')

    def test_read_roles(self):
        role1 = Role(role_name='Role 1', role_desc='This is role 1')
        role2 = Role(role_name='Role 2', role_desc='This is role 2')
        db.session.add_all([role1, role2])
        db.session.commit()
        response = self.app.post('/role/read')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Role 1', response.data)
        self.assertIn(b'Role 2', response.data)

    def test_update_role(self):
        role = Role(role_name='Test Role', role_desc='This is a test role')
        db.session.add(role)
        db.session.commit()
        response = self.app.post('/role/update', data=dict(name='Test Role', new_name='New Role', new_desc='This is the new role'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'updated successfully', response.data)
        role = Role.query.filter_by(role_name='New Role').first()
        self.assertIsNotNone(role)
        self.assertEqual(role.role_desc, 'This is the new role')

    def test_delete_role(self):
        role = Role(role_name='Test Role', role_desc='This is a test role')
        db.session.add(role)
        db.session.commit()
        response = self.app.post('/role/delete', data=dict(name='Test Role'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted successfully', response.data)
        role = Role.query.filter_by(role_name='Test Role').first()
        self.assertIsNone(role)

    def test_search_roles(self):
        role1 = Role(role_name='Role 1', role_desc='This is role 1')
        role2 = Role(role_name='Role 2', role_desc='This is role 2')
        db.session.add_all([role1, role2])
        db.session.commit()
        response = self.app.post('/role/search', data=dict(query='role'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Role 1', response.data)
        self.assertIn(b'Role 2', response.data)

    def test_apply_role(self):
        role = Role(role_name='Test Role', role_desc='This is a test role')
        staff = Staff(staff_id='123', staff_f_name='John', staff_l_name='Doe')
        db.session.add_all([role, staff])
        db.session.commit()
        response = self.app.post('/role/apply', data=dict(role_name='Test Role', staff_id='123'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully Applied', response.data)
        applicant = Role_Applicants.query.filter_by(role='Test Role', staff='123').first()
        self.assertIsNotNone(applicant)

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
    def test_create_hr_already_created(self):
        tester = app.test_client(self)
        response = tester.get('/create_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Already Created' in response.data)

    # HR Create Tests - Boundary Path 
    def test_create_hr_boundary(self):
        tester = app.test_client(self)

        # Test with smallest possible HR ID (assuming it's 1)
        response = tester.get('/create_hr/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Test with largest possible HR ID (assuming it's 10000)
        response = tester.get('/create_hr/10000', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    # HR Read Tests - Happy Path
    def test_read_hr(self):
        tester = app.test_client(self)
        response = tester.get('/read_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Read HR' in response.data)

    # HR Read Tests - Negative Path
    def test_read_hr_non_existent(self):
        tester = app.test_client(self)
        response = tester.get('/read_hr/9999', content_type='html/text')
        self.assertEqual(response.status_code, 404)

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
        response = tester.get('/update_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Update HR' in response.data)

    # HR Update Tests - Negative Path
    def test_update_hr_non_existent(self):
        tester = app.test_client(self)
        response = tester.get('/update_hr/9999', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    # HR Update Tests - Boundary Path
    def test_update_hr_boundary(self):
        tester = app.test_client(self)

        # Test with smallest possible HR ID (assuming it's 1)
        response = tester.get('/update_hr/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Test with largest possible HR ID (assuming it's 10000)
        response = tester.get('/update_hr/10000', content_type='html/text')
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

