# Model (table in db)
#Considered as a table to the Flask App'''
from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin
import pycountry


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True) # Needed for SQLAlchemy to understand each row in database
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50),nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60),nullable=False)
    balance = db.Column(db.Integer(), nullable=False, default = 1000)
    items = db.relationship('Item', backref='owned_user', lazy=True) #Allows us to see the owner of specific item

    @property
    def prettier_balance(self):
        if len(str(self.balance)) >= 4:
            return f'${str(self.balance)[:-3]},{str(self.balance)[-3:]}'
        else:
            return f"${self.balance}"
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plaintext_password):
        self.password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_purchase(self,item_obj):
        return self.balance >= item_obj.price
    
    def can_sell(self,item_obj):
        return item_obj in self.items
    
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(),nullable=False)
    barcode = db.Column(db.String(length=12),nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    origin_code = db.Column(db.String(length=2))
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    
    #To customise how item seen when queried in shell
    def __repr__(self):
        return f'Item {self.name}'
    
    def buy(self,user):
        self.owner = user.id # Assign ownership
        user.balance -= self.price
        db.session.commit()
    
    def sell(self,user):
        self.owner = None # remove ownership
        user.balance += self.price
        db.session.commit()
    
    def origin_decoder(self):
        country = pycountry.countries.get(alpha_2=self.origin_code.upper()).name
        if country:
            return country
        return "Unknown"
        
        
    
