from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Admin, School, Upload

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

# ---------- ADMIN LOGIN ----------
@bp.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid login details')
    return render_template('admin_login.html')

@bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# ---------- SCHOOL LOGIN ----------
@bp.route('/school', methods=['GET', 'POST'])
def school_login():
    if request.method == 'POST':
        login_id = request.form['login_id']
        password = request.form['password']
        school = School.query.filter_by(login_id=login_id, password=password).first()
        if school:
            return redirect(url_for('main.school_dashboard'))
        else:
            flash('Invalid school login')
    return render_template('school_login.html')

@bp.route('/school/dashboard')
def school_dashboard():
    uploads = Upload.query.all()
    return render_template('school_dashboard.html', uploads=uploads)
