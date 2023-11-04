import unittest
from app import app, db, Role, Role_Applicants

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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

        

if __name__ == '__main__':
    unittest.main()