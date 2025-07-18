from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User, Employee
from app import db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# --------------------------- Login ----------------------------------------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        employee_id = request.form.get('employee_id')  # NONE FOR ADMINS
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('auth.login'))

        if user.role == 'employee' and str(user.employee_id) != employee_id:
            flash('Incorrect employee ID', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Login successful', 'success')

        if user.role == 'admin':
            return redirect(url_for('payroll.admin_dashboard'))
        else:
            return redirect(url_for('payroll.employee_dashboard'))

    return render_template('login.html')


# ---------------- Register -------------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        username = request.form.get('username')

        # Check if employee exists
        employee = Employee.query.filter_by(id=employee_id).first()
        if not employee:
            flash("Invalid employee ID. Please contact admin.", "danger")
            return redirect(url_for('auth.register'))

        # Check if user already exists
        existing_user = User.query.filter_by(employee_id=employee_id).first()
        if existing_user:
            flash("An account already exists for this employee ID.", "danger")
            return redirect(url_for('auth.login'))

        # Create new user
        new_user = User(username=username, employee_id=employee_id)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! You can now log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')



# ----------------------- Logout -------------------------------

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
