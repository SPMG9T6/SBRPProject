# SBRPProject

# Skills-Based Role Portal

The Skills-Based Role Portal is a web application that allows All-In-One staff to apply for roles, view role-skill matches, browse and filter role listings, and enables human resource managers to maintain and view role listings and applicant skills.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

### Installation

To run the Skills-Based Role Portal, follow these steps:

Step 1: Clone the repository.

   ```bash
   git clone https://github.com/yourusername/skills-based-role-portal.git
   cd skills-based-role-portal
   ```
Step 2: Install the required dependencies.
```bash
   pip install -r requirements.txt --no-cache-dir
```
Step 3: Set up the database.
- Turn on your WAMP/MAMP server. 
- Access phpMyAdmin and create a new database or import the provided sbrpdb database.
   


### Usage 

How to run the Flask application:
Step 1: Open a terminal in VSC
Step 2: Initialise the database schema: 

python
from app import db
db.create_all()
exit()

Step 3: Start the Flask app

python app.py

Step 4: Access the portal by going to http://localhost:5000

Step 5: For direct access to HR View, you go to http://localhost:5000/hr
For direct access to Staff View, go to http://localhost:5000/staff

Step 6: To access unit tests, go to test_unit.py

### Features

Role Application: All-In-One staff can apply for roles and check their role-skill match.

Role Listings: HR managers can create, update, and browse role listings. HR managers can also view skills of role applicants. 

Skill Matching: The portal calculates and displays the percentage of matching skills between applicants and roles.

Database: The application uses a MySQL database to store and manage role listings and applicant information.




