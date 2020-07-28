
from flask import Flask, request, jsonify, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Employee

# @app.route("/")
# def hello():
#     return "Hello DevOps!"

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
            #return "Employee added. employee id={}".format(employee.id)
            return redirect("/")
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

@app.route("/")
def get_all():
    try:
        employees=Employee.query.all()
        return render_template("index.html",employee_html=employees)
    except Exception as e:
     return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        employee=Employee.query.filter_by(id=id_).first()
        return render_template("show.html",employee_html=employee)
    except Exception as e:
     return(str(e))
@app.route("/update/<id_>",methods=["GET","POST"])
def update(id_):
    employee=Employee.query.filter_by(id=id_).first()
    if request.method == "POST":
        try:
            name=request.form.get("newname")
            age=request.form.get("newage")
            address=request.form.get("newaddress")
            employee.name=name
            employee.age=age
            employee.address=address
            db.session.commit()
            return render_template("show.html",employee_html=employee)
        except Exception as e:
            return redirect("/")
    else:
        return render_template("update.html",employee=employee)
@app.route("/delete", methods=["POST"])
def delete():
    id= request.form.get("id")
    employee=Employee.query.filter_by(id=id).first()
    db.session.delete(employee)
    db.session.commit()
    flash("successfully removed")
    return redirect("/")
if __name__ == '__main__':
    app.run()
