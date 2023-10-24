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

           
if __name__ == '__main__':
    unittest.main()

