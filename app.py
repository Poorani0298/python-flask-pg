
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Employee

@app.route("/")
def hello():
    return "Hello DevOps!"

@app.route("/name/<name>")
def get_employee_name(name):
    return "name : {}".format(name)

@app.route("/details")
def get_employee_details():
    age=request.args.get('age')
    address=request.args.get('address')
    return "Age : {}, Address: {}".format(age,address)

@app.route("/add")
def add_employee():
    name=request.args.get('name')
    age=request.args.get('age')
    address=request.args.get('address')
    try:
        employee=Employee(
            name=name,
            age=age,
            address=address
        )
        db.session.add(employee)
        db.session.commit()
        return "Employee added. employee id={}".format(employee.id)
    except Exception as e:
     return(str(e))

@app.route("/add/form",methods=['GET', 'POST'])
def add_employee_form():
    if request.method == 'POST':
        name=request.form.get('name')
        age=request.form.get('age')
        address=request.form.get('address')
        try:
            employee=Employee(
                name=name,
                age=age,
                address=address
            )
            db.session.add(employee)
            db.session.commit()
            return "Employee added. employee id={}".format(employee.id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

@app.route("/getall")
def get_all():
    try:
        employees=Employee.query.all()
        return  jsonify([e.serialize() for e in employees])
    except Exception as e:
     return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        employee=Employee.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
     return(str(e))

if __name__ == '__main__':
    app.run()
