"""Models for PackTrack app. This python fields contain the model for my packTrack dataBase.

Classes included: User, Package, Status, Item

Tables included: users, packages, statuses, items

Table Relationships: User had many packages, Packages has one User
                     Package has many Statuses, Statuses has one Package
                     Package has many Itmes, Itmes are contained in one Package

MVP model conatins User and Package classes. 
2.0 will utilize Status and Item classes.

"""
## Import flask for using sqlAchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create that sqlAlchemy instance object
db = SQLAlchemy()


class User(db.Model):
    """ The User"""
    __tablename__ = "users" # tables name

    # Setting the tables fields and type.
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True,  nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname =db.Column(db.String(25), nullable=False)
    address =db.Column(db.String(50), nullable=False)
    city =db.Column(db.String(25), nullable=False)
    state =db.Column(db.String(25), nullable=False)
    zipcode =db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50),nullable=False)

    # Set the user table to a many package relationship
    packages = db.relationship("Package", back_populates="user")

    #set up the object repr for testing
    def __repr__(self):
        return f"<User user_id={self.user_id} fname={self.fname} email ={self.email}>"


class Package(db.Model):
    """ The Packages per user"""
    __tablename__ = "packages" # tables name

    # Setting the tables fields and type
    package_id = db.Column(db.Integer, autoincrement=True, primary_key=True,  nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False) #foreign key to users
    tracking_number= db.Column(db.String(100), nullable=False)
    shipped_date =db.Column(db.DateTime)
    location=db.Column(db.String(100), nullable=False)
    status =db.Column(db.String(100), nullable=False)
    merchant=db.Column(db.String(100))
    carrier =db.Column(db.String(100))

    # Set the packages table to a single user,many packages, many Items
    user = db.relationship("User", back_populates = "packages")
    statuses = db.relationship("Status", back_populates = "package")
    items = db.relationship("Item", back_populates = "package")

    #set up the object repr for testing
    def __repr__(self):
        return f"<Package package_id={self.package_id} tracking number={self.tracking_number} Status ={self.status}>"

class Status(db.Model):
    """ The statuses per package"""
    __tablename__ = "statuses" # tables name

    # Setting the tables fields
    status_id = db.Column(db.Integer, autoincrement=True, primary_key=True,  nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey("packages.package_id"), nullable=False) #foreign key to packages
    status = db.Column(db.String(100))
    date =db.Column(db.DateTime)

    # Set the statuses table to a single package
    package = db.relationship("Package", back_populates = "statuses")

    #set up the object repr for testing
    def __repr__(self):
        return f"<Status status_id={self.status} status={self.status} date ={self.date}>"

class Item(db.Model):
    """ The items per package"""
    __tablename__ = "items" # tables name

    # Setting the tables fields
    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True,  nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey("packages.package_id"), nullable=False) #foreign key to packages
    quantity = db.Column(db.Integer)
    name =db.Column(db.String)

    # Set the items table to a single package
    package = db.relationship("Package", back_populates = "items")

    #set up the object repr for testing
    def __repr__(self):
        return f"<Item item_id={self.quantity} name={self.name}>"



# function to connect to database
def connect_to_db(flask_app, db_uri="postgresql:///packTrack", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app) # app is your Flask object created in the server.py.