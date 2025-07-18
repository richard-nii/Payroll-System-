# app/seed.py
from app import create_app, db
from app.models import User, Employee, Grade, Department, Job, Element, Payroll
from datetime import date

app = create_app()

with app.app_context():
    # clean slate
    db.drop_all()
    db.create_all()

    # seed core data
    dept = Department(department_name="Engineering")
    grade = Grade(salary=5000.00)
    job = Job(job_name="Developer", job_description="Writes code")
    elem = Element(
        transport_allowance=300,
        utility_allowance=100,
        extra_duty_allowance=50,
        other_allowance=0,
        overtime=0,
        social_security_deduction=200,
        tax_deduction=150,
        loan1_deduction=0,
        loan2_deduction=0,
        other_deductions=0
    )
    db.session.add_all([dept, grade, job, elem])
    db.session.flush()

    emp = Employee(
        employee_id=1001,
        first_name="John",
        surname="Doe",
        date_of_birth=date(1990,1,1),
        grade_id=grade.grade_id,
        department_id=dept.department_id,
        job_id=job.job_id,
        element_id=elem.element_id,
        bank_name="ABC Bank",
        bank_account_number="123456789"
    )
    db.session.add(emp)
    db.session.flush()

    user_admin = User(username="admin", role="admin", employee_id=emp.employee_id)
    user_emp = User(username="johndoe", role="employee", employee_id=emp.employee_id)

    db.session.add_all([user_admin, user_emp])
    db.session.commit()

    print("✅ Seeded admin and employee successfully.")
