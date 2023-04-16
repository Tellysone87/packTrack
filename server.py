"""Server for the PackTrack App"""
# Import the needed libraries for webpage server.

# Flask is a web framework used to repsond to requests.
# I will using flask to handle calls when forms are submitted.
# Flask responds to web requests by calling functions
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify , json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import os
import requests

# Jinja is a popular template system for Python, used by Flask.
# we will use this to make a template for each of your webpages.
# They would then inherit the base html.
from jinja2 import StrictUndefined

# import db to start connecting to database
from model import connect_to_db, db
import crud
import fed_Api


# Creating a object of Flask to use in our site
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.config.from_pyfile('config.cfg') # imports the mail server info
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

# home.html route. It loads the homepage
@app.route('/home.html')
def load_homepage():
    """loads the home page """

    return render_template("home.html")

# Below is the route for my log in page.
@app.route('/login.html')
def user_sign_in():
    """ loads sign in page"""

    return render_template("login.html")

# loads the register page
@app.route('/register.html')
def user_registry():
    """ loads register page"""

    return render_template("register.html")

#helper function to check for empty fields, returned boolean
def check_empty_fields(field_list):
    """ Checks if any of the list fields are empty"""
    for field in field_list:
        if field == "":
            return False
        else:
            return True

# route to handle form with /users Post method (register.html)
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
    fields = [fname, lname, address, city, state, email, password] # list of user giving values
   
    # check if fields are empty
    if check_empty_fields(fields) == False: #this is our helper fucntion
        flash("All fields are required to make an account. Try again.")
        return redirect("/register.html") # tell user to fill all fields out and redirect
    
    # Check if user exists by email before allowing a new account to be created. 
    if user:
        flash("A account exists with this email. Cannot create an account with that email. Try again.")
    else:
    # create that user account by adding that new object instance
        user = crud.create_user(fname, lname, address, city, state, email, password)
        # add user to the db session and commit
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.") #notify user of new account

    return redirect("/")

# route to handle form with /login Post method (login.html)
@app.route('/login', methods=["POST"])
def user_signin():
    """ Checks to verify users password"""

    # grabs the fields info
    email = request.form.get("email")
    password = request.form.get("password")

    # sets user to the function to get user by email
    user = crud.get_user_by_email(email)
    
    #Check if user exist first or the server will error
    if user:
        # condition for password entry
        correct_password = user.password # the correct password is the one in our Databse under the user.
        if (password == correct_password): # correct password steps
            flash(f"Successfully signed in. Welcome back, {user.fname}!")
            session["user_email"] = user.email
            return redirect("/tracking.html")
        elif not user or password != correct_password: # incorrect password steps
            flash("Your password or username is incorrect. Try again.")
            return redirect("/login.html")
    # If that user does not exist. Ask the user to try again of create a new account.
    elif not user:
        flash("There is no registered user with this email address. Please try again or create an account.")
        return redirect("/login.html")
      
# route to load the profile page with the user info
@app.route('/profile.html')
def load_profile_page():
    """ renders profile page for the logged in User"""
    user = crud.get_user_by_email(session["user_email"]) #grabs user from the cookie session
    print(user)

    return render_template("/profile.html",user=user) # render profile and pass that user object

# route to handle form with /tracking Post method (tracking.html)
@app.route('/tracking', methods=['POST'])
def track_package():
    """ Creates new package record with the tracking number provided"""
    
    #grab the tracking number submitted by signed in user
    package_to_track = request.form.get("tracking")
    # identify user signed in
    user = crud.get_user_by_email(session["user_email"])

    # gets the Fedex api json for the package by calling fed_Api function
    try: # try to track if not return message
     info = fed_Api.get_tracking_info(package_to_track) # returns library
    except KeyError: 
        flash(f'We are not able to track package number {package_to_track} at this time.')
        return redirect('/tracking.html')

    # grabs the information needed from the api library I created
    user_id = user
    tracking_number = info['tracking']
    shipped_date = info['shipped']
    location = info['location']
    status = info['status']
    merchant = info['merchant']
    carrier = info['carrier']
    

    # Takes those values and adds them to the create package methods arguments
    new_pack = crud.create_package(user_id=user_id.user_id, tracking_number=tracking_number,
                                   shipped_date=shipped_date, location=location, status=status,
                                   merchant=merchant, carrier=carrier)

    # add the package record to database
    db.session.add(new_pack)
    db.session.commit()

    # call the load history helper function once package is created to grab that tracking number.
    load_all_package_history(tracking_number)

    # redirects with new package added
    return redirect('/tracking.html')

# function to populate statuses table based per package. It will be called
# in the tracing Post route. 
def load_all_package_history(tracking_number):
    """ helper function to add histry to the statuses table"""
    # store the package Statuses as well
    history = fed_Api.get_events_info(tracking_number) # list of package status update
    print(history)
    
    # loop through through each status and add it as a new status record using the same package id and commit the changes.
    for new_status in history.values():
        #grab the fields out of the library
        package = crud.get_package_by_tracking(tracking_number) # set the statuses to the correct package
        new_status['track'] = package
        new_stat = crud.create_status(package_id = new_status.get('track'), status = new_status.get('event'), date = new_status.get('date'))
        db.session.add(new_stat)
        db.session.commit()

@app.route('/history', methods = ['POST'])
def send_ajax_history():

    # grab the tracking number from row submitted
    track_pack = request.json.get("track_pack")
    print(track_pack)

    #get the package id to pull statuses
    history = fed_Api.get_events_info(track_pack)
    print(history)
    status = jsonify(history)
    print(status)
    
    return status
    

# route to display tracking page
@app.route('/tracking.html')
def load_tracking_page():
    """ renders profile page"""

    # grab user signed in
    user = crud.get_user_by_email(session["user_email"])
    # grab all packages connected to that user
    packages = crud.get_packages_by_user(user.user_id)

    return render_template("tracking.html", packages=packages) #return trackage with the packages

# route to handle form with /profile Post method (profile.html). TO ADD- prompt to ensure user wants to change profile fields
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

    # the field is updated where the user adds a new value
    if fname != "":
        user.fname = fname
    elif lname != "":
        user.lname = lname
    elif address != "":
        user.address = address
    elif city != "":
        user.city = city
    elif state != "":
        user.state = state
    elif email != "":
        user.email = email

    db.session.commit() # commit those changes. 
    session["user_email"] = user.email #reset the new email as the users in session now
    flash("Your account has been updated")
    return redirect("/profile.html") # redirect and show changes. 

# route to display reset password page
@app.route('/reset_password.html')
def load_reset_password():
    """render in reset page"""
    return render_template("reset_password.html")

# route to handle form with /reset_password Post method (reset_password.html). This also
# creates and send the email security token to the users email. 
# TO ADD - make the email and link look better
# TO ADD - add a link back to the register page
@app.route('/reset_password', methods=["POST"])
def reset_password():
    """render in reset page"""

    # grab the email submitted
    email = request.json.get("email")
    user = crud.get_user_by_email(email) # sets the email to user if user exists
    
    #if user, set the email as a secret token and prompt user to check their email for link
    if user:
        token = s.dumps(email, salt='reset_email_link') # create the token for user email
        msg = Message('Click here to reset your password',
                      sender='superstaris2020@gmail.com', recipients=[email]) # set the message to send, my email, and the users email
        link = url_for('reset_email_link', token=token, _external=True) # link with email token and it is outside our app thus external
        msg.body = 'Your link is {}'.format(link) # email body with link. 
        mail.send(msg) # Send email 

        return {"current_user": True}
    else:
        return {"current_user": False}

# route for getting that toekn form the email and checking if it is correct before 
# directing user to set their new password. TO ADD have the errors load back to the reset page with alerts
@app.route('/set_password.html/<token>')
def reset_email_link(token):
    """checks token and lets user reset their password"""

    # catch if the link is expire or token is not correct
    try:
        email = s.loads(token, salt='reset_email_link', max_age=4600)
    except SignatureExpired: # Expired
        return '<h1> Your link has expired</h1>'
    except BadTimeSignature: # Token link not correct
        return '<h1> You are not the correct user</h1>'
    # if it is correct display this
    return render_template('/set_password.html', email = email )

# route for displaying set password page. 
@app.route('/set_password.html')
def set_new_password():
    """allows the user to reset their passwork with form"""
    
    return render_template('/set_password.html')

# route to handle form with /set_new_password Post method (set_password.html).
@app.route('/set_new_password', methods =['POST'])
def grab_password_value():
    """Grabs and set the new password value"""

    #get form date. If this page is loaded the user must have clicked the email token link in time.
    email = request.form.get("email")
    password = request.form.get("password")
    new_password = request.form.get("new_password")

    #set the user that needs the password updated
    user = crud.get_user_by_email(email)
    if user:
        if password == new_password: # if email is confirmed 
            user.password = password # set new password
            db.session.commit() # commit change to database
            flash("Your password has been reset. Please log in. ")
            return redirect("/login.html") # redirect user to now sign in
        
        elif password != new_password: # if passwords don't match, ask the user to try again
            flash("Your passwords do not match. You must confirm your password.")
            return redirect('/set_password.html')
    #if the user puts in wrong email redirect and ask them to try again 
    elif not user:
        flash("Your email is incorrect, please try again.")
        return redirect('/set_password.html')


# Creating Flask object to use on our site.
# tells Python to execute code if you’re running a script directly.
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
