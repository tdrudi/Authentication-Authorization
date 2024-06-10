from flask import Flask, render_template, redirect, session
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback"
app.config['SQLALCHEM_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)

@app.route("/")
def homepage():
    """Redirect to register"""
    return redirect("/register")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Register a user, show and handle form submission"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        """On form submission"""
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")
    
    else:
        return render_template("register.html", form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login form and handle submission"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        """On form submission"""
        username = form.username.data
        password = form.password.data
        
        """Authenticate user login"""
        user = User.authenticate(username, password)
    
        if user:
            """If user login correct"""
            session['username'] = user.username
            return redirect(f"/users/{user.username}") 
       
        else:
            """If user login incorrect or not logged in"""
            form.username.errors = ['Invalid Login']
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logout user and redirect to login page"""
    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):
    """Show user page""" 
    if "username" not in session or username != session['username']:
        """User is not logged in or a different user is logged in"""
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("show_user.html", user = user, form = form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Remove user and redirect to login page""" 

    if "username" not in session or username != session['username']:
        """User is not logged in or a different user is logged in"""
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods = ['GET', 'POST'])
def new_feedback(username):
    """Add feedback form and handle submission"""
    if "username" not in session or username != session['username']:
        """User is not logged in or a different user is logged in"""
        raise Unauthorized()
    
    form = FeedbackForm()
    if form.validate_on_submit():
        """On form submission"""
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title = title, content = content, username = username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("new_feedback.html", form=form)
    
@app.route("/feedback/<int:feedback_id>/update", methods=["GET","POST"])
def edit_feedback(feedback_id):
    """Show feedback form and handle submission"""
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        """User is not logged in or a different user is logged in"""
        raise Unauthorized()
    
    form = FeedbackForm(obj = feedback)

    if form.validate_on_submit():
        """On form submission"""
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    
    return render_template("edit_feedback.html", form = form, feedback = feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback and redirect to user page"""   
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        """User is not logged in or a different user is logged in"""
        raise Unauthorized()
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        
    return redirect(f"/users/{feedback.username}")
