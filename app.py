from flask import Flask, render_template, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
app.static_folder = 'static'
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                            'root:root' + \
                                            '@localhost:3306/sbrpdb'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                               'pool_recycle': 280}
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()


# Database Code 
class Access_Control(db.Model):
    __tablename__ = 'access_control'

    access_id = db.Column(db.Integer, primary_key=True)
    access_control_name = db.Column(db.String(20), nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.access_control_name}"

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_f_name = db.Column(db.String(50), nullable=False)
    staff_l_name = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('access_control.access_id'),
        nullable=False)

    def __repr__(self) -> str:
        return f"{self.staff_f_name}"

class Skill(db.Model):
    __tablename__ = 'skill'
    skill_name = db.Column(db.String(20), primary_key=True)
    skill_desc = db.Column(db.Text(), nullable=False)

    def __repr__(self) -> str:
        return f"{self.skill_name}"

class Staff_Skill(db.Model):
    __tablename__ = 'staff_skill'

    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'),
        primary_key=True)
    skill_name = db.Column(db.Integer, db.ForeignKey('skill.skill_name'),
        primary_key=True)
    staff = db.relationship('Staff', backref='skills')
    skill = db.relationship('Skill')

    def __repr__(self) -> str:
        return f"{self.skill_name}"

class Role(db.Model):
    __tablename__ = 'role'
    role_name = db.Column(db.String(20), primary_key=True)
    role_desc = db.Column(db.Text(), nullable=False)


    def __repr__(self) -> str:
        return f"{self.role_name}"

class Role_Skill(db.Model):
    __tablename__ = 'role_skill'
    role_name = db.Column(db.Integer, db.ForeignKey('role.role_name'),
        primary_key=True)
    skill_name = db.Column(db.Integer, db.ForeignKey('skill.skill_name'),
        primary_key=True)
    

    def __repr__(self) -> str:
        return f"{self.role_name}-{self.skill_name}"

class Role_Applicants(db.Model):
    __tablename__ = 'role_applicants'

    sno = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, db.ForeignKey('role.role_name'),
        nullable=False)
    staff = db.Column(db.Integer, db.ForeignKey('staff.staff_id'),
        nullable=False)
    

    def __repr__(self) -> str:
        return f"{self.role}-{self.staff}"

class Role_Listing(db.Model):
    __tablename__ = 'role_listing'
    role_name = db.Column(db.Integer, db.ForeignKey('role.role_name'),
        primary_key=True)
    deadline = db.Column(db.Integer,
        primary_key=True)
    department = db.Column(db.String(20))
    

    def __repr__(self) -> str:
        return f"{self.role_name}-{self.deadline}"
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(50), db.ForeignKey('staff.staff_id'), nullable=False)
    staff_f_name = db.Column(db.String(50), db.ForeignKey('staff.staff_f_name'), nullable=False)
    staff_l_name = db.Column(db.String(50), db.ForeignKey('staff.staff_l_name'), nullable=False)
    email = db.Column(db.String(50), db.ForeignKey('staff.email'), nullable=False)
    country = db.Column(db.String(50), db.ForeignKey('staff.country'), nullable=False)
    role_name = db.Column(db.String(50), db.ForeignKey('role.role_name'), primary_key=True)

    def __init__(self, role_name, staff_id, staff_f_name, staff_l_name, email, country):
        self.role_name = role_name
        self.staff_id = staff_id
        self.staff_f_name = staff_f_name
        self.staff_l_name = staff_l_name
        self.email = email
        self.country = country
    
    
# app route decorator to home page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        if role == 'staff':
            return redirect(url_for('view_roles'))
        elif role == 'hr':
            return redirect(url_for('update_roles'))
    return render_template('index.html')

@app.route('/staff')
def view_roles():
    # Query the database to get a list of role listings
    roles = db.session.query(Role.role_name, Role.role_desc, Role_Listing.deadline, Role_Listing.department) \
        .join(Role_Listing, Role.role_name == Role_Listing.role_name) \
        .all()
    
    role_skills = db.session.query(Role_Skill.role_name, Role_Skill.skill_name).all()

    staff_id = 140001  # Specify the staff_id for which you want to check skills
    staff_skills = set()  # Use a set to store staff skills

    # Query the skills for the specific staff_id
    for skill_name, in db.session.query(Staff_Skill.skill_name).filter(Staff_Skill.staff_id == staff_id):
        staff_skills.add(skill_name)

    # Create a dictionary to store skill names for each role
    role_skill_dict = {}
    for role_name, skill_name in role_skills:
        if role_name not in role_skill_dict:
            role_skill_dict[role_name] = []
        role_skill_dict[role_name].append(skill_name)

    applications = Application.query.all()

    def assign_color(department):
        color_map = {
            "Consultancy": "bg-primary",
            "Engineering": "bg-secondary",
            "Finance": "bg-danger",
            "HR": "bg-warning",
            "IT": "bg-info",
            "Sales": "bg-success",
            "Solutioning": "bg-dark",
        }
        return color_map.get(department, "bg-light")

    return render_template('view_roles.html', roles=roles, applications=applications, role_skill_dict=role_skill_dict, staff_skills=staff_skills, assign_color=assign_color)

@app.route('/hr')
def update_roles():
    # Query the database to get a list of role listings
    # Query the database to get a list of role listings
    roles = db.session.query(Role.role_name, Role.role_desc, Role_Listing.deadline, Role_Listing.department) \
        .join(Role_Listing, Role.role_name == Role_Listing.role_name) \
        .all()
    
    applications = Application.query.all()

    def assign_color(department):
        color_map = {
            "Consultancy": "bg-primary",
            "Engineering": "bg-secondary",
            "Finance": "bg-danger",
            "HR": "bg-warning",
            "IT": "bg-info",
            "Sales": "bg-success",
            "Solutioning": "bg-dark",
        }
        return color_map.get(department, "bg-light")

    return render_template('update_roles.html', roles=roles, applications=applications, assign_color=assign_color)



#staff apply for role
@app.route('/apply_role', methods=['GET', 'POST'])
def apply_role():
    if request.method == 'POST':
        role_name = request.form['role_name']
        staff_id = request.form['staff_id']
        staff_f_name = request.form['staff_fname']
        staff_l_name = request.form['staff_lname']
        email = request.form['email']
        country = request.form['country']

        # Save the application details to the database
        application = Application(role_name=role_name, staff_id=staff_id, staff_f_name=staff_f_name, staff_l_name=staff_l_name, email=email, country=country)
        db.session.add(application)
        db.session.commit()

        return redirect(url_for('thank_you'))  # Redirect to the thank you page

    # If the request method is GET, render the form
    role_name = request.args.get('role_name')

    # Fetch a list of distinct countries from the staff table
    countries = db.session.query(Staff.country).distinct().all()
    countries = [country[0] for country in countries]  # Extract country names
    return render_template('apply_role.html', role_name=role_name, countries=countries)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')



@app.route('/add_role_listing/create', methods=['GET', 'POST'])
def add_role_listing():
    if request.method == 'POST':
        role_name = request.form['role_name']
        deadline = request.form['deadline']
        department = request.form['department']

        new_role_listing = Role_Listing(role_name=role_name, deadline=deadline, department=department)

        # Add the role listing to the database
        db.session.add(new_role_listing)
        db.session.commit()

        resp = {'response':'Role Listing Created Successfully', 'role_name':role_name, 'deadline':deadline, 'department':department}
        return render_template('response.html', resp=resp)
    
    return render_template('add_role_listing.html', deadline=deadline, roles=role_name)

@app.route('/get_skills', methods=['GET'])
def get_skills():
    # Fetch the list of skills from your database or another data source
    skills = Skill.query.all()  # Assuming you have a Skill model

    # Convert the skills to a format suitable for JSON response
    skill_list = [{'skill_name': skill.skill_name, 'skill_desc': skill.skill_desc} for skill in skills]

    return jsonify(skill_list)

@app.route('/get_roles', methods=['GET'])
def get_roles():
    # Fetch the list of roles from your database or another data source
    roles = Role.query.all()  # Assuming you have a Role model

    # Convert the roles to a format suitable for JSON response
    role_list = [{'role_name': role.role_name, 'role_desc': role.role_desc} for role in roles]

    return jsonify(role_list)

@app.route('/edit_role_listing/<role_name>', methods=['GET', 'POST'])
def edit_role_listing(role_name):
    role_listing = Role_Listing.query.filter_by(role_name=role_name).first()
    all_roles = Role.query.all()  # Fetch all available roles for the dropdown

    if request.method == 'POST':
        role_listing.deadline = request.form['deadline']

        db.session.commit()

        return redirect(url_for('update_roles'))

    return render_template('edit_role_listing.html', role_listing=role_listing, all_roles=all_roles)

@app.route('/get_role_skill', methods=['GET'])
def get_role_skill():
    role_name = request.args.get('roleName')
    
    # Query the database to get the skill for the role
    role_skill = Role_Skill.query.filter_by(role_name=role_name).first()
    
    if role_skill:
        # If the role skill is found, return its skill name
        return jsonify({'skill_name': role_skill.skill_name})
    else:
        # Return an error response if the role skill is not found
        return jsonify({'error': 'Role skill not found'})
    
@app.route('/view_role_skill_match')
def view_role_skill_match():
    return render_template('view_role_skill_match.html')



@app.route('/view_applicants')
def view_applicants():
    applications = db.session.query(Application).all()

    application_data = []

    for application in applications:
        application_info = {
            'role_name': application.role_name,
            'staff_name': f"{application.staff_f_name} {application.staff_l_name}",
            'staff_skills': [],
            'role_skills': [],
            'matching_skills': [],
            'role_skill_match': 0.0,
        }

        staff_skills = db.session.query(Staff_Skill).filter(Staff_Skill.staff_id == application.staff_id).all()
        application_info['staff_skills'] = [skill.skill_name for skill in staff_skills]

        role_skills = db.session.query(Role_Skill).filter(Role_Skill.role_name == application.role_name).all()
        application_info['role_skills'] = [skill.skill_name for skill in role_skills]

        matching_skills = set(application_info['staff_skills']) & set(application_info['role_skills'])
        application_info['matching_skills'] = list(matching_skills)

        # Calculate role skill match percentage
        total_role_skills = len(application_info['role_skills'])
        if total_role_skills > 0:
            role_skill_match = (len(matching_skills) / total_role_skills) * 100
            application_info['role_skill_match'] = round(role_skill_match, 2)

        application_data.append(application_info)

    return render_template('applicants.html', applications=application_data)
        
if __name__ == "__main__":
    app.run(debug=True)

