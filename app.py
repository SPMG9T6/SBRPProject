from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
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

CORS(app)

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

    sno = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), nullable=False)
    skill_desc = db.Column(db.Text(), nullable=False)

    def __repr__(self) -> str:
        return f"{self.skill_name}"

class Staff_Skill(db.Model):
    __tablename__ = 'staff_skill'

    sno = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'),
        nullable=False)
    skill_name = db.Column(db.Integer, db.ForeignKey('skill.sno'),
        nullable=False)

    def __repr__(self) -> str:
        return f"{self.skill_name}"

class Role(db.Model):
    __tablename__ = 'role'
    sno = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=False)
    role_desc = db.Column(db.Text(), nullable=False)


    def __repr__(self) -> str:
        return f"{self.role_name}"

class Role_Skill(db.Model):
    __tablename__ = 'role_skill'

    sno = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.Integer, db.ForeignKey('role.sno'),
        nullable=False)
    skill_name = db.Column(db.Integer, db.ForeignKey('skill.sno'),
        nullable=False)
    

    def __repr__(self) -> str:
        return f"{self.role_name}-{self.skill_name}"

class Role_Applicants(db.Model):
    __tablename__ = 'role_applicants'

    sno = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, db.ForeignKey('role.sno'),
        nullable=False)
    staff = db.Column(db.Integer, db.ForeignKey('staff.staff_id'),
        nullable=False)
    

    def __repr__(self) -> str:
        return f"{self.role}-{self.staff}"
    
class Role_Listings(db.Model):
    __tablename__ = 'role_listings'
    role_name = db.Column(db.String(50), primary_key=True)
    role_desc = db.Column(db.String(255))
    skill_name = db.Column(db.String(50), primary_key=True)

    def __repr__(self) -> str:
        return f"RoleListings('{self.role_name}', '{self.role_desc}', '{self.skill_name}')"


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
                new_entry = Role_Applicants(role=or_role.sno, staff=or_staff.staff_id)
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
                # skills_of_applicatant = Staff_Skill.query.filter_by(staff_id = all_applicants.staff)
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
                all_roles = Roll_Skill.query.filter_by(role_name=role_id)
                skills_required = [Skill.query.filter_by(sno=row.skill_name).first().skill_name for row in all_roles]
                
                all_applicants = Role_Applicants.query.filter_by(role = role_id)
                # skills_of_applicatant = Staff_Skill.query.filter_by(staff_id = all_applicants.staff)
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
            

if __name__ == "__main__":
    app.run(debug=True)

