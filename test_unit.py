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


# Staff View Tests

    def test_view_employee(self):
        tester = app.test_client(self)
        response = tester.get('/view_employee', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'View Employee' in response.data)    

# Staff Browse Testing

    def test_browse_employee(self):
        tester = app.test_client(self)
        response = tester.get('/browse_employee', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Browse Employee' in response.data)


# Staff Filter roles Testing

    def test_filter_roles(self):
        tester = app.test_client(self)
        response = tester.get('/filter_roles', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Filter Roles' in response.data)

# Staff Filter department Testing

    def test_filter_department(self):
        tester = app.test_client(self)
        response = tester.get('/filter_department', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Filter Department' in response.data)

# Staff Apply Testing

    def test_apply(self):
        tester = app.test_client(self)
        response = tester.get('/apply', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Apply' in response.data)


# Hr View Tests

    def test_view_hr(self):
        tester = app.test_client(self)
        response = tester.get('/view_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'View HR' in response.data)

# HR CRU TESTS - Create, Read, Update

# HR Create Tests
    def test_create_hr(self):
        tester = app.test_client(self)
        response = tester.get('/create_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Create HR' in response.data)

# HR Read Tests

    def test_read_hr(self):

        tester = app.test_client(self)
        response = tester.get('/read_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Read HR' in response.data)

# HR Update Tests

    def test_update_hr(self):

        tester = app.test_client(self)
        response = tester.get('/update_hr', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Update HR' in response.data)








if __name__ == '__main__':
    unittest.main()

