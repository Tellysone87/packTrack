"""CRUD operations."""

""" 
This is my Crud.py file. 
It conatins the following db functions:
create user - Creates a new user.
create package - creates a new package.
create status - creates a new status.
create item = creates a new item.
get package by user - returns the users packages by user_id.

---------------------------2.0 section of web app ---------------------------------------------
get status by package - returns that package current status.
get item in package - returns the packages item. 

"""

from model import db, User, Package, Status,Item, connect_to_db
from datetime import datetime

def create_user(fname,lname,address,city,state,email, password):
    """his function Creates and return a new user."""

    user = User(
        fname=fname,
        lname=lname,
        address=address,
        city=city,
        state=state,
        email=email, 
        password=password
        )

    return user


def create_package(user_id,tracking_number,shipped_date,location,status,merchant,carrier):
    """Create and return a new package."""

    package = Package(
       user_id = user_id,
       tracking_number = tracking_number,
       shipped_date = shipped_date,
       location = location,
       status = status,
       merchant = merchant,
       carrier = carrier
        )

    return package

def create_status(package_id,status,date):
    """Create and return a new status."""

    status= Status(
       package_id = package_id,
       status = status,
       date = date
        )

    return status

def create_item(package_id,quantity,name):
    """Create and return a new status."""

    item= Item(
       package_id = package_id,
       quantity = quantity,
       name = name
        )

    return item

def get_packages_by_user(user_id):
    """ returns the list of packages for the user"""
    package_list = [] # create empty list
    specific_user = user_id # variable to hold user id

    tracked_package = User.query.get(specific_user).packages # grabs the users packages

    # loop to grab each package and add to the empty array
    for package in tracked_package:
        package_list.append(package)
        print(f"Your tracking number is {package.tracking_number} and it is {package.status}.")
    
    return package_list # return the list of packages


def status_by_package(package_id):
    """ returns the past statuses of a package"""
    status_list = [] # create empty list
    specific_package = package_id # variable to hold user id

    package_statuses = Package.query.get(specific_package).statuses # grabs the users packages

    # loop to grab each package and add to the empty array
    for status in package_statuses:
        status_list.append(status)
    
    return status_list # return the list past package statuses

def item_in_package(package_id):
    """ returns the items of a package"""
    item_list = [] # create empty list
    specific_package = package_id # variable to hold package id

    package_items = Package.query.get(specific_package).items # grabs the users packages

    # loop to grab each item and add to the empty array
    for item in package_items:
        item_list.append(item)
    
    return item_list # return the list of items

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()
    
   


# grabbing our connect ot bd function and passing our flask object
if __name__ == "__main__":
    from server import app

    connect_to_db(app)