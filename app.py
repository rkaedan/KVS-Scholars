from flask import Flask, render_template, request

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return "Welcome to KVS Scholars!"

# Admin login page
@app.route('/admin')
def admin_login():
    return "Admin login page"

# School login page
@app.route('/school')
def school_login():
    return "School login page"

if __name__ == "__main__":
    app.run(debug=True)
