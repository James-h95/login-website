from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, PurchaseItemForm, LoginForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required,current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required # Redirects user to login page first
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object: # if not null, apply ownership
            if current_user.can_purchase(p_item_object): # Verify curr user can afford it
                p_item_object.buy(current_user)
                flash(f"Congratulations, you purchased the {p_item_object.name} for ${p_item_object.price}!",category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase the {p_item_object.name}!",category='danger')
                
        # Sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object: # If not null, remove ownership
            if current_user.can_sell(s_item_object): # Verify if user owns this item
                s_item_object.sell(current_user)
                flash(f"Congratulations, you sold the {s_item_object.name} back to the market!",category='success')
            else:
                flash(f"Something went wrong with selling the {s_item_object.name}",category='danger')
        return redirect(url_for('market_page'))
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None) # Only show items which have not been purchased by anyone
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items, purchase_form=purchase_form, owned_items=owned_items,selling_form=selling_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm() #create instance of it
    if form.validate_on_submit(): # Verify to execute only after user press submit
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data, 
                              password=form.password1.data) 

        
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create) 
        flash(f"Account created successfully! You are logged in as {user_to_create.username}",category="success")
        
        return redirect(url_for('market_page'))
    
    if form.errors != {}: #if there are errors from validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm() # create instance of it
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as:{attempted_user.username}',category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password dont match! Please try again',category='danger')
            
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!',category='info')
    return redirect(url_for("home_page"))