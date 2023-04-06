"""Server for the PackTrack App"""
# Import the needed libraries for webpage server.

# Flask is a web framework used to repsond to requests. 
# I will using flask to handle calls when forms are submitted.
# Flask responds to web requests by calling functions
from flask import Flask, render_template, request, flash, session, redirect

# Jinja is a popular template system for Python, used by Flask.
# we will use this to make a template for each of your webpages. 
# They would then inherit the base html.
from jinja2 import StrictUndefined

# import db to start connecting to database
from model import connect_to_db, db
import crud


# Creating a object of Flask to use in our site
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# We also need to handle routing requests. 
# Routes tell Flask which URL should correspond with which function. 
# Below is the route for my homepage.
@app.route('/')
def load_page():
    """loads home page for testing"""

    return render_template("home.html")

# Below is the route for my log in page.
@app.route('/login.html')
def user_sign_in():
    """ loads sign in page"""

    return render_template("login.html")

@app.route('/register.html')
def user_registry():
    """ loads register page"""

    return render_template("register.html")

@app.route('/users', methods = ["POST"])
def register_user():
    """ accepts fields from register page to create new user"""

    #grab the fields info
    fname=request.form.get("fname"),
    lname=request.form.get("lname")
    address=request.form.get("address"),
    city=request.form.get("city"),
    state=request.form.get("state"),
    email=request.form.get("email"), 
    password=request.form.get("password")

    #sets user to the function to get user by email
    user = crud.get_user_by_email(email)

    # Chack if user exixts
    if user:
        flash("A account exists with this email. Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(fname,lname,address,city,state,email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
        
    return redirect("/")

@app.route('/login',methods = ["POST"])
def user_signin():
    """ Checks to verify users password"""
    # grabs the field info
    email=request.form.get("email"), 
    password=request.form.get("password")

    #sets user to the function to get user by email
    user = crud.get_user_by_email(email)
    correct_password = user.password
    
    # condition for password entry
    if (password == correct_password):
        flash(f"Successfully signed in. Welcome back, {user.fname}!")
        session["user_email"] = user.email
        return render_template("tracking.html")
    elif not user or password != correct_password:
        flash("Your password or username is incorrect. Try again.")
        return redirect("/login.html")

@app.route('/profile.html')
def load_profile_page():
    """ renders profile page"""
    user = crud.get_user_by_email(session["user_email"])

    return render_template("profile.html", user = user)

@app.route('/tracking.html')
def load_tracking_page():
    """ renders profile page"""
    user = crud.get_user_by_email(session["user_email"])
    packages = crud.get_packages_by_user(user.user_id)

    return render_template("tracking.html",packages = packages)

@app.route('/profile', methods =["POST"])
def update_profile():
    #set the user at top
    user = crud.get_user_by_email(session["user_email"])
    
    #grab the fields info
    fname=request.form.get("fname")
    lname=request.form.get("lname")
    address=request.form.get("address")
    city=request.form.get("city")
    state=request.form.get("state")
    email=request.form.get("email")

    if fname != "":
        user.fname = fname
    if lname != "":
        user.lname = lname
    if address != "":
        user.address = address
    if city != "":
        user.city = city
    if state != "":
        user.state = state
    if email != "":
        user.email = email

    db.session.commit()
    return redirect("profile.html")


# Creating Flask object to use on our site. 
if __name__ == "__main__": #tells Python to execute code if you’re running a script directly.
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)