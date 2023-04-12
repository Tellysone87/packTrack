"""Server for the PackTrack App"""
# Import the needed libraries for webpage server.

# Flask is a web framework used to repsond to requests.
# I will using flask to handle calls when forms are submitted.
# Flask responds to web requests by calling functions
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_mail import Mail, Message
import fed_Api
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import os
import requests
import smtplib

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
app.config.from_pyfile('config.cfg')
mail = Mail(app)

# create serializer and give it the app secret key
s = URLSafeTimedSerializer(app.secret_key)

# We also need to handle routing requests.
# Routes tell Flask which URL should correspond with which function.
# Below is the route for my homepage.


@app.route('/')
def load_page():
    """loads home page for testing"""

    return render_template("home.html")


@app.route('/home.html')
def load_homepage():
    """loads the home page """

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


def check_empty_fields(field_list):
    """ Checks if any of the list fields are empty"""
    for field in field_list:
        if field == "":
            return False
        else:
            return True


@app.route('/users', methods=["POST"])
def register_user():
    """ accepts fields from register page to create new user"""

    # grab the fields info
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    email = request.form.get("email")
    password = request.form.get("password")

    # sets user to the function to get user by email
    user = crud.get_user_by_email(email)
    fields = [fname, lname, address, city, state, email, password]
    print(fields)

    # check if fields are empty
    if check_empty_fields(fields) == False:
        flash("All fields are required to make an account. Try again.")
        return redirect("/register.html")
    # Check if user exists
    if user:
        flash("A account exists with this email. Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(fname, lname, address,
                                city, state, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route('/login', methods=["POST"])
def user_signin():
    """ Checks to verify users password"""
    # grabs the field info
    email = request.form.get("email")
    password = request.form.get("password")

    # sets user to the function to get user by email
    user = crud.get_user_by_email(email)
    correct_password = user.password
   
    # condition for password entry
    if (password == correct_password):
        flash(f"Successfully signed in. Welcome back, {user.fname}!")
        session["user_email"] = user.email
        return redirect("/tracking.html")
    elif not user or password != correct_password:
        flash("Your password or username is incorrect. Try again.")
        return redirect("/login.html")


@app.route('/profile.html')
def load_profile_page():
    """ renders profile page for the logged in User"""
    user = crud.get_user_by_email(session["user_email"])

    return render_template("profile.html", user=user)


@app.route('/tracking', methods=['POST'])
def track_package():
    """ Creates new package record with the tracking number provided"""
    package_to_track = request.form.get("tracking")
    # identify user signed in
    user = crud.get_user_by_email(session["user_email"])
    # gets the Fedex api json for the package
    info = fed_Api.get_tracking_info(package_to_track)

    # grabs the information needed from the api library I created
    user_id = user
    tracking_number = info['tracking']
    shipped_date = info['shipped']
    location = info['location']
    status = info['status']
    merchant = info['merchant']
    carrier = info['carrier']

    # Takes those values and adds them to the create package methods arguements
    new_pack = crud.create_package(user_id=user_id.user_id, tracking_number=tracking_number,
                                   shipped_date=shipped_date, location=location, status=status,
                                   merchant=merchant, carrier=carrier)

    # add the package record
    db.session.add(new_pack)
    db.session.commit()
    # redirects with new package added
    return redirect('/tracking.html')


@app.route('/tracking.html')
def load_tracking_page():
    """ renders profile page"""
    user = crud.get_user_by_email(session["user_email"])
    packages = crud.get_packages_by_user(user.user_id)

    return render_template("tracking.html", packages=packages)


@app.route('/profile', methods=["POST"])
def update_profile():
    # set the user at top
    user = crud.get_user_by_email(session["user_email"])

    # grab the fields info
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    email = request.form.get("email")

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
    flash("Your account has been updated")
    return redirect("/profile.html")


@app.route('/reset_password.html')
def load_reset_password():
    """render in reset page"""
    return render_template("reset_password.html")

@app.route('/reset_password', methods=["POST"])
def reset_password():
    """render in reset page"""
    email = request.form.get("email")
    user = crud.get_user_by_email(email)
    if user:
        flash("Please check your email for the reset link.")
        # create the token for user email
        token = s.dumps(email, salt='reset_email_link')
        # print("##############################################")
        # print(email)
        # print(token
        msg = Message('Click here to reset your password',
                      sender='superstaris2020@gmail.com', recipients=[email])
        link = url_for('reset_email_link', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)

        # message = '<p>click here to reset your password.</p>'
        # server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        # server.starttls()
        # server.login(gmail, gmail_password)
        # server.sendmail(gmail,email,message)
        return redirect("reset_password.html")
    else:
        flash("No account exists with the provided email. Please create an account")
        return redirect("/login.html")


@app.route('/set_password.html/<token>')
def reset_email_link(token):
    """checks token and lets user reset their password"""
    print(token)
    # catch if the kin is expire or token is not correct
    try:
        email = s.loads(token, salt='reset_email_link', max_age=4600)
    except SignatureExpired:
        return '<h1> Your link has expired</h1>'
    except BadTimeSignature:
        return '<h1> You are not the correct user</h1>'

    print(email)
    # if it is correct display this
    return render_template('/set_password.html', email = email )


@app.route('/set_password.html')
def set_new_password():
    """allows the user to reset their passwork with form"""
    
    return render_template('/set_password.html')

@app.route('/set_new_password', methods =['POST'])
def grab_password_value():
    """Grabs and set the new password value"""
    email = request.form.get("email")
    password = request.form.get("password")
    new_password = request.form.get("new_password")

    #set the user that needs the password updated
    user = crud.get_user_by_email(email)
    if user:
        if password == new_password:
            user.password = password
            db.session.commit()
            flash("Your password has been reset. Please log in. ")
            return redirect("/login.html")
        elif password != new_password:
            flash("Your passwords do not match. You must confirm your password.")
            return redirect('/set_password.html')
    elif not user:
        flash("Your email is incorrect, please try again.")
        return redirect('/set_password.html')


# Creating Flask object to use on our site.
# tells Python to execute code if you’re running a script directly.
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
