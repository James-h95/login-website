# Model (table in db)
#Considered as a table to the Flask App'''
from market import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True) # Needed for SQLAlchemy to understand each row in database
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50),nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60),nullable=False)
    balance = db.Column(db.Integer(), nullable=False, default = 1000)
    items = db.relationship('Item', backref='owned_user', lazy=True) #Allows us to see the owner of specific item



class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(),nullable=False)
    barcode = db.Column(db.String(length=12),nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    #To customise how item seen when queried in shell
    def __repr__(self):
        return f'Item {self.name}'
    
