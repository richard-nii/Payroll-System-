from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from flask_login import login_required, current_user
from app.models import Employee, Payroll, Grade, Department, Job, Element, db
from app import db
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

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



# ----------------------- MANAGE DEPARTMENTS -----------------------------------

@payroll_bp.route('/admin/departments', methods=['GET', 'POST'])
@login_required
def manage_departments():
    if request.method == 'POST':
        department_name = request.form['name']
        description = request.form.get('description')

        if Department.query.filter_by(department_name=department_name).first():
            flash('Department already exists!', 'danger')
        else:
            new_dept = Department(department_name=department_name)
            db.session.add(new_dept)
            db.session.commit()
            flash('Department created successfully!', 'success')
            return redirect(url_for('payroll.manage_departments'))

    departments = Department.query.all()
    return render_template('departments.html', departments=departments)



@payroll_bp.route('/admin/departments/delete/<int:id>', methods=['POST'])
@login_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('Department deleted successfully.', 'success')
    return redirect(url_for('payroll.manage_departments'))



# ----------------------MANAGE GRADE ------------------------

@payroll_bp.route('/admin/grades', methods=['GET', 'POST'])
@login_required
def manage_grades():
    if request.method == 'POST':
        grade_name = request.form['grade_name']
        salary = request.form['salary']

        if Grade.query.filter_by(grade_name=grade_name).first():
            flash('Grade already exists!', 'danger')
        else:
            try:
                new_grade = Grade(grade_name=grade_name, salary=float(salary))
                db.session.add(new_grade)
                db.session.commit()
                flash('Grade added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding grade: {e}', 'danger')

        return redirect(url_for('payroll.manage_grades'))

    grades = Grade.query.all()
    return render_template('grades.html', grades=grades)


@payroll_bp.route('/grades/delete/<int:id>', methods=['POST'])
def delete_grade(id):
    grade = Grade.query.get_or_404(id)
    db.session.delete(grade)
    db.session.commit()
    flash('Grade deleted successfully.', 'success')
    return redirect(url_for('payroll.manage_grades'))


# ----------------------- MANAGE JOBS ----------------------

@payroll_bp.route('/admin/jobs', methods=['GET', 'POST'])
def manage_jobs():
    if request.method == 'POST':
        job_name = request.form.get('job_name')
        if job_name:
            new_job = Job(job_name=job_name)
            db.session.add(new_job)
            db.session.commit()
            flash('Job added successfully', 'success')
        return redirect(url_for('payroll.manage_jobs'))

    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)


@payroll_bp.route('/admin/jobs/delete/<int:id>', methods=['POST'])
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully', 'success')
    return redirect(url_for('payroll.manage_jobs'))


# ---------------------------- MANAGE ELEMENT -----------------------

@payroll_bp.route('/manage_elements', methods=['GET', 'POST'])
@login_required
def manage_elements():
    if request.method == 'POST':
        # Read values from form
        transport = float(request.form.get('transport_allowance', 0))
        utility = float(request.form.get('utility_allowance', 0))
        extra_duty = float(request.form.get('extra_duty_allowance', 0))
        other_allow = float(request.form.get('other_allowance', 0))
        overtime = float(request.form.get('overtime', 0))

        ssd = float(request.form.get('social_security_deduction', 0))
        tax = float(request.form.get('tax_deduction', 0))
        loan1 = float(request.form.get('loan1_deduction', 0))
        loan2 = float(request.form.get('loan2_deduction', 0))
        other_ded = float(request.form.get('other_deductions', 0))

        # Create and save new element
        element = Element(
            transport_allowance=transport,
            utility_allowance=utility,
            extra_duty_allowance=extra_duty,
            other_allowance=other_allow,
            overtime=overtime,
            social_security_deduction=ssd,
            tax_deduction=tax,
            loan1_deduction=loan1,
            loan2_deduction=loan2,
            other_deductions=other_ded
        )
        db.session.add(element)
        db.session.commit()
        flash('New element added successfully!', 'success')
        return redirect(url_for('payroll.manage_elements'))

    elements = Element.query.all()
    return render_template('manage_elements.html', elements=elements)



# --------------------- PAYROLL ------------------------------------

def calculate_payroll(employee):
    grade_salary = employee.grade.salary
    element = employee.element 

    allowance_total = element.allowances or 0
    deduction_total = element.deductions or 0

    net_pay = grade_salary + allowance_total - deduction_total

    return {
        'basic_salary': grade_salary,
        'allowances': allowance_total,
        'deductions': deduction_total,
        'net_pay': net_pay
    }


# ------------------- PAYROLL RECORDS -----------------------------

@payroll_bp.route('/admin/generate_payroll', methods=['GET', 'POST'])
@login_required
def generate_payroll():
    if request.method == 'POST':
        month = request.form.get('month')
        year = int(request.form.get('year'))
        employees = Employee.query.all()

        for emp in employees:
            grade = emp.grade
            element = emp.element

            if not grade or not element:
                continue  # Skip if data is incomplete

            base_salary = grade.salary or 0
            allowances = (
                element.transport_allowance +
                element.utility_allowance +
                element.extra_duty_allowance +
                element.other_allowance +
                element.overtime
            )

            deductions = (
                element.social_security_deduction +
                element.tax_deduction +
                element.loan1_deduction +
                element.loan2_deduction +
                element.other_deductions
            )

            gross = base_salary + allowances
            net = gross - deductions

            payroll = Payroll(
                employee_id=emp.employee_id,
                grade_id=emp.grade_id,
                element_id=emp.element_id,
                month=month,
                year=year,
                gross_salary=gross,
                total_deductions=deductions,
                net_pay=net
            )
            db.session.add(payroll)

        db.session.commit()
        flash('Payroll generated successfully.', 'success')
        return redirect(url_for('payroll.admin_dashboard'))

    return render_template('generate_payroll.html')




# ------------------ VIEW PAYROLL RECORDS -------------------------------

@payroll_bp.route('/admin/payroll-records')
def view_payroll_records():
    records = Payroll.query.order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    return render_template('payroll_records.html', records=records)



# -------------------- VIEW PAYSLIPS -------------------------------------

@payroll_bp.route('/employee/payslips')
@login_required
def view_payslips():
    if current_user.role != 'employee':
        return redirect(url_for('payroll.admin_dashboard'))

    payslips = Payroll.query.filter_by(employee_id=current_user.employee_id).order_by(
        Payroll.year.desc(), Payroll.month.desc()
    ).all()

    return render_template('view_payslips.html', payslips=payslips)



# ------------------------ DOWNLOAD PAYSLIPS -------------------------------------

@payroll_bp.route('/employee/payslip/<int:payroll_id>/download')
@login_required
def download_payslip(payroll_id):
    payslip = Payroll.query.filter_by(payroll_id=payroll_id, employee_id=current_user.employee_id).first()

    if not payslip:
        flash("Payslip not found", "danger")
        return redirect(url_for('payroll.view_payslips'))

    # PDF creation
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Header
    p.drawString(100, 750, "Payslip")
    p.drawString(100, 735, f"Name: {payslip.employee.first_name} {payslip.employee.surname}")
    p.drawString(100, 720, f"Employee ID: {payslip.employee.employee_id}")
    p.drawString(100, 705, f"Period: {payslip.month} {payslip.year}")

    # Payroll Details
    p.drawString(100, 680, f"Basic Salary: {payslip.gross_salary - payslip.total_deductions:.2f}")
    p.drawString(100, 665, f"Gross Salary: {payslip.gross_salary:.2f}")
    p.drawString(100, 650, f"Total Deductions: {payslip.total_deductions:.2f}")
    p.drawString(100, 635, f"Net Pay: {payslip.net_pay:.2f}")

    p.showPage()
    p.save()

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=payslip_{payslip.month}_{payslip.year}.pdf'
    return response
