from flask import Flask, render_template, request, redirect, session, url_for
from models import db, User
import pickle
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ✅ Load trained model
model_path = "model/career_model.pkl"
model = pickle.load(open(model_path, "rb")) if os.path.exists(model_path) else None

# ✅ Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        school = request.form["school"]

        # Save user to DB
        user = User(name=name, email=email, school=school)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect(url_for("dashboard"))
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))
        else:
            return "User not found", 404
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/assessment', methods=["GET", "POST"])
def assessment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == "POST":
        user.skills = request.form["skills"]
        user.interests = request.form.get("interests", "")
        user.recommended = request.form.get("recommended", "")
        db.session.commit()
        return redirect(url_for("results"))
    return render_template('assessment.html', user=user)

@app.route('/results')
def results():
    if "user_id" not in session or not model:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    if user.skills:
        prediction = model.predict([user.skills])[0]
        confidence = max(model.predict_proba([user.skills])[0]) * 100
        recommendation = [{
            "name": prediction,
            "score": round(confidence, 2),
            "description": "A potential match based on your skill set."
        }]
    else:
        recommendation = []
    return render_template('results.html', recommendations=recommendation)

@app.route('/profile-settings', methods=["GET", "POST"])
def profile_settings():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    user = User.query.get(session['user_id'])
    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]
        user.skills = request.form.get("skills", "")
        user.interests = request.form.get("interests", "")
        user.recommended = request.form.get("recommended", "")
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template('profile_settings.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
