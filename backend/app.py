from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True, nullable=False)
    role_description = db.Column(db.Text(), unique=True, nullable=False)
    
    def __init__(self, role_name, role_description):
        self.role_name = role_name
        self.description = role_description
        return '<Roles %r>' % self.role

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)