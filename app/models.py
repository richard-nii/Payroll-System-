from . import db
from flask_login import UserMixin


# ------------------------------
# 1. User Table
# ------------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.Enum('admin', 'employee'), nullable=False)

# ------------------------------
# 2. Employee Table
# ------------------------------
class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.Integer, primary_key=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.grade_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'))
    element_id = db.Column(db.Integer, db.ForeignKey('element.element_id'))
    first_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    bank_name = db.Column(db.String(100))
    bank_account_number = db.Column(db.String(100))

    user = db.relationship('User', backref='employee', uselist=False)

# ------------------------------
# 3. Grade Table
# ------------------------------
class Grade(db.Model):
    __tablename__ = 'grade'

    grade_id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Numeric(10, 2))
    
    employees = db.relationship('Employee', backref='grade', lazy=True)
    payrolls = db.relationship('Payroll', backref='grade', lazy=True)


# ------------------------------
# 4. Department Table
# ------------------------------
class Department(db.Model):
    __tablename__ = 'department'

    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    
    employees = db.relationship('Employee', backref='department', lazy=True)


# ------------------------------
# 5. Job Table
# ------------------------------
class Job(db.Model):
    __tablename__ = 'job'

    job_id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    
    employees = db.relationship('Employee', backref='job', lazy=True)


# ------------------------------
# 6. Element Table
# ------------------------------
class Element(db.Model):
    __tablename__ = 'element'

    element_id = db.Column(db.Integer, primary_key=True)
    transport_allowance = db.Column(db.Numeric(10, 2))
    utility_allowance = db.Column(db.Numeric(10, 2))
    extra_duty_allowance = db.Column(db.Numeric(10, 2))
    other_allowance = db.Column(db.Numeric(10, 2))
    overtime = db.Column(db.Numeric(10, 2))
    social_security_deduction = db.Column(db.Numeric(10, 2))
    tax_deduction = db.Column(db.Numeric(10, 2))
    loan1_deduction = db.Column(db.Numeric(10, 2))
    loan2_deduction = db.Column(db.Numeric(10, 2))
    other_deductions = db.Column(db.Numeric(10, 2))
    
    employees = db.relationship('Employee', backref='element', lazy=True)
    payrolls = db.relationship('Payroll', backref='element', lazy=True)


# ------------------------------
# 7. Payroll Table
# ------------------------------
class Payroll(db.Model):
    __tablename__ = 'payroll'

    payroll_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.grade_id'), nullable=False)
    element_id = db.Column(db.Integer, db.ForeignKey('element.element_id'), nullable=False)

    employee = db.relationship('Employee', backref='payroll')

