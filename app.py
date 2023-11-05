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
    roles = Role_Listing.query.all()
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


# create role
@app.route("/role/<action>", methods=['GET','POST'])
def role_action(action):
    if request.method == 'POST':
        if action == "create":
            role_name = request.form['role_name']
            role_desc = request.form['role_desc']
            new_role = Role(role_name=role_name, role_desc=role_desc)
            db.session.add(new_role)
            db.session.commit()
            resp = {'response':'create successfully', 'role_name':role_name, 'role_desc':role_desc}
            return render_template('response.html', resp=resp)

        elif action == "read":
            all_role = Role.query.all()
            if all_role:
                resp = [{'role_name':row.role_name,'role_desc':row.role_desc} for row in all_role]
            return jsonify(resp)

        elif action == "update":
            all_role = Role.query.filter_by(role_name=request.form['name']).first()
            if all_role:
                role_name = request.form['new_name']
                role_desc = request.form['new_desc']
                if role_name:
                    all_role.role_name = role_name
                if role_desc:
                    all_role.role_desc = role_desc
                db.session.commit()
                resp = {'response':'updated successfully', 'role_name':role_name, 'role_desc':role_desc}
                return resp
            else:
                resp = {'response':'wrong role name'}
                return resp

        elif action == "delete":
            all_role = Role.query.filter_by(role_name=request.form['name']).first()
            if all_role:
                db.session.delete(all_role)
                db.session.commit()
                resp = {'response':'deleted successfully'}
                return resp
            else:
                resp = {'response':'wrong role name'}
                return resp

        elif action == "search":
            all_role = Role.query.filter((Role.role_name.contains(request.form['query'])) | (Role.role_desc.contains(request.form['query'])))
            if all_role:
                resp = []
                for row in all_role:
                    resp = [{'role_name':row.role_name,'role_desc':row.role_desc} for row in all_role]
                return resp
            else:
                resp = {'response':'no! data available'}
                return resp

        elif action == "apply":
            role_name = request.form['role_name']
            staff_id = request.form['staff_id']
            or_role = Role.query.filter_by(role_name=role_name).first()
            or_staff = Staff.query.filter_by(staff_id=staff_id).first()
            if or_role and or_staff:
                new_entry = Role_Applicants(role=or_role.role_name, staff=or_staff.staff_id)
                db.session.add(new_entry)
                db.session.commit()
                resp = {'response': f'{or_staff.staff_f_name} Successfully Applied for {or_role.role_name}'}
                return resp
            else:
                resp = {'response':'something wrong'}
                return resp
        
@app.route('/role-applicant-skills/<action>', methods=['GET','POST'])
def skills_of_role_applicants(action):
    # skills applicant have skill applicant dont have
    if request.method == 'POST':
        if action == "read":
            role_name = request.form['role_name']
            role_id = Role.query.filter_by(role_name=role_name)
            if role_id:
                role_id = role_id.first().sno
                all_applicants = Role_Applicants.query.filter_by(role = role_id)
                # skills_of_applicant = Staff_Skill.query.filter_by(staff_id = all_applicants.staff)
                resp = []
                for i in all_applicants:
                    all_skills = []
                    all_skills_query = Staff_Skill.query.filter_by(staff_id=i.staff)
                    for j in all_skills_query:
                        all_skills.append(Skill.query.filter_by(sno=j.skill_name).first().skill_name)
                    resp.append({'name':Staff.query.filter_by(staff_id=i.staff).first().staff_f_name, 'skills':all_skills})
                return resp
            else:
                resp = {'response':'wrong role name'}
                return resp

        

@app.route('/applicant-skills-match/<action>', methods=['GET','POST'])
def applicant_skills_match(action):
    # skills applicaent have skill applicatent dont have
    if request.method == 'POST':
        if action == "check":
            role_name = request.form['role_name']
            role_id = Role.query.filter_by(role_name=role_name)
            if role_id:
                role_id = role_id.first().sno
                all_roles = Role_Skill.query.filter_by(role_name=role_id)
                skills_required = [Skill.query.filter_by(sno=row.skill_name).first().skill_name for row in all_roles]
                
                all_applicants = Role_Applicants.query.filter_by(role = role_id)
                # skills_of_applicant = Staff_Skill.query.filter_by(staff_id = all_applicants.staff)
                resp = []

                for i in all_applicants:
                    skills_match = []
                    skills_not_match = []
                    staff_skills = []

                    all_skills_query = Staff_Skill.query.filter_by(staff_id=i.staff)
                    
                    for j in all_skills_query:
                        skill_name = Skill.query.filter_by(sno=j.skill_name).first().skill_name
                        staff_skills.append(skill_name)
                        if skill_name in skills_required:
                            skills_match.append(skill_name)
                        else:
                            skills_not_match.append(skill_name)
                    resp.append({'name':Staff.query.filter_by(staff_id=i.staff).first().staff_f_name,'staff_skills':staff_skills, 'skills_required':skills_required, 'skills_match':skills_match, 'skills_not_match':skills_not_match})
                return resp
            else:
                resp = {'response':'wrong role name'}
                return resp
            

# Route to add a new role listing

@app.route('/add_role_listing/create', methods=['GET', 'POST'])
def add_role_listing():
    if request.method == 'POST':
        role_name = request.form['role_name']
        deadline = request.form['deadline']
        department = request.form['department']

        # Create a new role listing
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
        # Update other details
        role_listing.deadline = request.form['deadline']

        # Commit changes to the database
        db.session.commit()

        # Redirect to the view roles page or any other suitable page
        return redirect(url_for('update_roles'))

    # Render the edit role listing form with the role name and all available roles
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

@app.route('/role_skill_match', methods=['GET', 'POST'])
def role_skill_match():
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        role_name = request.form.get('role_name')
    else:
        staff_id = request.args.get('staff_id')
        role_name = request.args.get('role_name')

    if staff_id and role_name:
        # Query the staff's skills from the database
        staff_skills = Staff_Skill.query.filter_by(staff_id=staff_id).all()

        # Query the required skills for the role from the database
        role_skills = Role_Skill.query.filter_by(role_name=role_name).all()

        # Extract skill names
        staff_skill_names = [staff_skill.skill_name for staff_skill in staff_skills]
        role_skill_names = [role_skill.skill_name for role_skill in role_skills]

        # Check for role-skill matches
        matches = [skill_name for skill_name in staff_skill_names if skill_name in role_skill_names]

        if request.method == 'POST':
            return render_template('view_role_skill_match.html', staff_id=staff_id, role_name=role_name, role_skill_matches=matches)
        else:
            return jsonify({'role_skill_match': matches})
    else:
        return jsonify({'error': 'Missing parameters'})
    


@app.route('/view_applicants')
def view_applicants():
    # Query the database to get a list of applicants and their skills
    applicants = db.session.query(Application, Staff_Skill).join(
        Staff_Skill, Application.staff_id == Staff_Skill.staff_id).all()

    return render_template('applicants.html', applicants=applicants)
        
if __name__ == "__main__":
    app.run(debug=True)

