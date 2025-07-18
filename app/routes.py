from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Employee, Payroll, Grade, Department, Job, Element, db
from app import db
from datetime import datetime

payroll_bp = Blueprint('payroll', __name__)


@payroll_bp.route('/')
def home():
    return redirect(url_for('auth.login'))


# ----------------------- ADMIN ------------------------------------

@payroll_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('payroll.employee_dashboard'))

    employees = Employee.query.all()
    return render_template('admin_dashboard.html', employees=employees)


# ----------------------- EMPLOYEE ---------------------------------

@payroll_bp.route('/employee/dashboard')
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        return redirect(url_for('payroll.admin_dashboard'))

    employee = Employee.query.filter_by(employee_id=current_user.employee_id).first()
    return render_template('employee_dashboard.html', employee=employee)


# ------------------------- EMPLOYEE UPDATES -----------------------------

@payroll_bp.route('/employee/update', methods=['POST'])
@login_required
def update_employee():
    if current_user.role != 'employee':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('payroll.admin_dashboard'))

    employee = Employee.query.filter_by(employee_id=current_user.employee_id).first()

    # Update editable fields
    employee.first_name = request.form['first_name']
    employee.surname = request.form['surname']
    employee.bank_name = request.form['bank_name']
    employee.bank_account_number = request.form['bank_account_number']

    db.session.commit()
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('payroll.employee_dashboard'))


# ---------------------- ADD EMPLOYEE ------------------------------

@payroll_bp.route('/admin/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        try:
            employee = Employee(
                employee_id=request.form['employee_id'],
                first_name=request.form['first_name'],
                surname=request.form['surname'],
                date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d'),
                grade_id=request.form['grade_id'],
                department_id=request.form['department_id'],
                job_id=request.form['job_id'],
                element_id=request.form['element_id'],
                bank_name=request.form['bank_name'],
                bank_account_number=request.form['bank_account_number']
            )
            db.session.add(employee)
            db.session.commit()
            flash('✅ Employee added successfully', 'success')
            return redirect(url_for('payroll.admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error: {e}', 'danger')

    grades = Grade.query.all()
    departments = Department.query.all()
    jobs = Job.query.all()
    elements = Element.query.all()
    return render_template('add_employee.html', grades=grades, departments=departments, jobs=jobs, elements=elements)
