import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app = Flask(__name__)
app.secret_key = "kvs_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kvs.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# ---------- Database Models ----------
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login_id = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    clas = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    chapter = db.Column(db.String(50), nullable=True)

# Create DB tables
with app.app_context():
    db.create_all()
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- Helper ----------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template("home.html")

# ---------- Admin ----------
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials!")
    return render_template("admin_login.html")

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        # Upload textbooks/notes
        file = request.files['file']
        clas = request.form['class']
        subject = request.form['subject']
        chapter = request.form['chapter']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            upload = Upload(filename=filename, clas=clas, subject=subject, chapter=chapter)
            db.session.add(upload)
            db.session.commit()
            flash("File uploaded successfully!")
        else:
            flash("Invalid file type!")
    return render_template("admin_dashboard.html")

@app.route('/admin/register_school', methods=['POST'])
def register_school():
    name = request.form['name']
    login_id = request.form['login_id']
    password = request.form['password']
    if School.query.filter_by(login_id=login_id).first():
        flash("Login ID already exists!")
    else:
        school = School(name=name, login_id=login_id, password=password)
        db.session.add(school)
        db.session.commit()
        flash("School registered successfully!")
    return redirect(url_for('admin_dashboard'))

# ---------- School ----------
@app.route('/school', methods=['GET', 'POST'])
def school_login():
    if request.method == 'POST':
        login_id = request.form['login_id']
        password = request.form['password']
        school = School.query.filter_by(login_id=login_id, password=password).first()
        if school:
            uploads = Upload.query.all()
            return render_template("school_dashboard.html", uploads=uploads, school=school)
        else:
            flash("Invalid school login!")
    return render_template("school_login.html")
