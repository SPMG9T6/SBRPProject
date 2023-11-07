import unittest
import json
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import unittest
from app import app, db, Role, Role_Applicants, Staff, Role_Listing, Application, Role_Skill, Staff_Skill, Skill, calculate_skill_match_percentage

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                            'root:root' + \
                                            '@localhost:3306/sbrpdb'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_role_listing(self):
        # Send a POST request to create a role with a department
        response = self.app.post('/add_role_listing/create', data=dict(role_name='Test Role', department='Test Dept', deadline='2023-12-12'))

        # Check the HTTP status code
        self.assertEqual(response.status_code, 200)

        # Check if the role has been added to the database
        role_listing = Role_Listing.query.filter_by(role_name='Test Role').first()
        self.assertIsNotNone(role_listing)
        self.assertEqual(role_listing.department, 'Test Dept')

    def test_update_role_listing(self):
        # Create a role listing in the database
        role_listing = Role_Listing(role_name='Test Role', department='Test Dept', deadline='2023-12-12')
        db.session.add(role_listing)
        db.session.commit()

        # Send a POST request to update the role listing
        response = self.app.post('/edit_role_listing/Test Role', data=dict(deadline='2024-01-01', department='Updated Department'))

        # Check the HTTP status code
        self.assertEqual(response.status_code, 302)

        # Query the updated role listing from the database
        updated_role_listing = Role_Listing.query.filter_by(role_name='Test Role').first()

        # Assert that the role listing was updated
        self.assertIsNotNone(updated_role_listing)
        self.assertEqual(updated_role_listing.deadline, '2024-01-01')
        self.assertEqual(updated_role_listing.department, 'Updated Department')



    def test_delete_role_listing(self):
        # Create a role listing
        role_listing = Role_Listing(role_name='Test Role', department='Test Dept', deadline='2023-12-12')
        db.session.add(role_listing)
        db.session.commit()

        # Send a GET request to delete the role listing
        response = self.app.get('/delete_role_listing/Test Role', follow_redirects=True)

        # Try to find the role listing in the database after deletion
        role_listing = Role_Listing.query.filter_by(role_name='Test Role').first()

        # Assert that the role listing is None (indicating it was deleted)
        self.assertIsNone(role_listing)

    # Staff Apply Role Testing - Happy Path
    def test_apply_role_post(self):
            # Simulate a POST request with form data
            response = self.app.post('/apply_role', data=dict(
                role_name='Test Role',
                staff_id='14001',
                staff_fname='Test F',
                staff_lname='Test L',
                email='test@gmail.com',
                country='SG'
            ), follow_redirects=True)  # Ensure you follow redirects

            self.assertEqual(response.status_code, 200)  # Check if it's a successful response code (update based on your actual implementation)

            # Check if the application has been added to the database
            application = Application.query.filter_by(role_name='Test Role').first()  # Assuming you have an Application model
            self.assertIsNotNone(application)
            self.assertEqual(application.staff_id, '14001')

    def test_apply_role_get(self):
        # Simulate a GET request to render the form
        response = self.app.get('/apply_role', query_string={'role_name': 'Test Role'})

        self.assertEqual(response.status_code, 200)  # Check if it's a successful response code (update based on your actual implementation)
        # You can also add more assertions here to check the content of the rendered template if needed.

    # View applicants
    def test_view_applicants(self):
        response = self.app.get('/view_applicants')
        self.assertEqual(response.status_code, 200)

    def test_calculate_skill_match_percentage(self):
        role_skills = ['Skill1', 'Skill2', 'Skill3']
        staff_skills = ['Skill2', 'Skill3', 'Skill4']

        role_skill_match = calculate_skill_match_percentage(role_skills, staff_skills)

        self.assertEqual(role_skill_match, 66.67)  # You should adjust this based on your expected result
if __name__ == '__main__':
    unittest.main()

