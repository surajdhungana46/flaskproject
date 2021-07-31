from classflask import app,db, bcrypt
from flask import render_template, url_for, flash, redirect, request,session
import random
from flask_uploads import UploadSet, configure_uploads, IMAGES
from classflask.forms import  RegistrationForm, LoginForm,AddProduct, AddToCart,Checkout
from classflask.model import User,Product,Order,Order_Item
from flask_wtf.file import FileField, FileAllowed
from flask_login import login_user, current_user, logout_user, login_required
import json
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
configure_uploads(app, photos)
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
def calculationcart():
    products = []
    grand_total = 0
    index = 0
    quantity_total=0

    for item in session['cart']:
        product = Product.query.filter_by(id=item['id']).first()

        quantity = int(item['quantity'])  
        total = quantity * product.price
        grand_total += total
        quantity_total+=quantity
        products.append({'id' : product.id, 'name' : product.name, 'price' :  product.price, 'image' : product.image, 'quantity' : quantity, 'total': total, 'index': index})
        index += 1
    
    delivery_charge = grand_total + 100
    return products, grand_total,  delivery_charge, quantity_total
@app.route("/")
def homepage():
    products = Product.query.all()
    return render_template('homepage.html',products=products,title='Home')

@app.route('/product/<id>')
def product(id):
    product = Product.query.filter_by(id=id).first()
    form=AddToCart()
    return render_template('view-product.html', product=product,form=form)


    

# @app.route("/dashboard", methods = ['GET',"POST"])
# def dashboard():
#     if request.method=="POST":
#         username = request.form.get("uname")
#         userpass = request.form.get("pass")
#         if username==params['admin_user'] and userpass==params['admin_password']:
#             return render_template("admin/index.html",params=params)
#             pass
#     else:
#         return render_template("adminlogin.html",params=params)
@app.route("/register", methods=['POST','GET' ])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =  RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('homepage'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
      
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))




    #cart 
@app.route('/quick-add/<id>')
def quick_add(id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'id' : id, 'quantity' : 1})
    session.modified = True

    return redirect(url_for('homepage'))
@app.route('/addcart', methods=['POST'])
def addcart():
    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()

    if form.validate_on_submit():

        session['cart'].append({'id' : form.id.data, 'quantity' : form.quantity.data})
        session.modified = True

    return redirect(url_for('homepage'))

@app.route('/cart')
def cart():
    products, grand_total, delivery_charge, quantity_total = calculationcart()

    return render_template('cart.html', products=products, grand_total=grand_total,   delivery_charge=delivery_charge,quantity_total=quantity_total)

@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = Checkout()

    products, grand_total, delivery_charge, quantity_total = calculationcart()

    if form.validate_on_submit():

        order = Order()
        form.populate_obj(order)
        order.reference = ''.join([random.choice('ABCDE12345') for _ in range(10)])
        order.status = 'PENDING'

        for product in products:
            order_item = Order_Item(quantity=product['quantity'], product_id=product['id'])
            order.items.append(order_item)

        db.session.add(order)
        db.session.commit()

        session['cart'] = []
        session.modified = True

        return redirect(url_for('homepage'))

    return render_template('checkout.html', form=form, grand_total=grand_total, delivery_charge=delivery_charge, quantity_total=quantity_total)

#  Admin routing

# @app.route('/Admin')
# def Admin():
#     all_data = Data.query.all()
 
#     return render_template("admindash.html", items = all_data)
 
 

# @app.route('/insert', methods = ['POST'])
# def insert():
#     if request.method == 'POST':

#         title = request.form['title']
#         price = request.form['price']
#         Description = request.form['Description']
#         image_large=request.form[' image_large']
  
#         my_data = Data(title, price, description,image_large)
#         db.session.add(my_data)
#         db.session.commit()
 
#         flash("Item Inserted Successfully")
 
#         return redirect(url_for('Admin'))
 

# @app.route('/update', methods = ['GET', 'POST'])
# def update():
 
#     if request.method == 'POST':
#         my_data = Data.query.get(request.form.get('itemid'))
 
#         my_data.title = request.form['name']
#         my_data.price = request.form['email']
#         my_data.Description = request.form['Description']
#         my_data.request.form[' image_large']
 
#         db.session.commit()
#         flash("Item Updated Successfully")
 
#         return redirect(url_for('Admin'))
 
 
 

# @app.route('/delete/<itemid>/', methods = ['GET', 'POST'])
# def delete(id):
#     my_data = Data.query.get(itemid)
#     db.session.delete(my_data)
#     db.session.commit()
#     flash("Item Deleted Successfully")
 
#     return redirect(url_for('Admin'))

# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

# @app.route("/dashboard", methods = ['GET',"POST"])
# def dashboard():
#    

@app.route("/dashlogin",methods=['GET','POST'])
# @login_required
def dashlogin():
    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        print(username)
        print(userpass)
        print (params['admin_user'])
        if username==params['admin_user'] and userpass==params['admin_password']:
            return redirect(url_for('admin'))
            pass
    else:
        return render_template("adminlogin.html",params=params)
        # return render_template("adminlogin.html")
    # error = None
    # if request.method == 'POST':
    #     if request.form['username'] != 'suraj' or request.form['password'] != 'suraj':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #         return redirect(url_for('admin'))
    # return render_template('adminlogin.html', error=error)
    # form=LoginForm()
    # if form.validate_on_submit():
    #     if form.email.data=='suraj@gmail.com' and form.email.password=='suraj':
    #         return redirect(url_for('admin'))
    # else:
    #     flash('Login Unsuccessful. Please check email and password', 'danger')
            
    # return render_template('adminlogin.html', form=form)
@app.route('/admin')
# @login_required
def admin():
    products = Product.query.all()
    orders = Order.query.all()

    return render_template('admin/index.html',products=products,orders=orders) 


 
@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddProduct()

    if form.validate_on_submit():
        image = photos.save(form.image.data)

        new_product = Product(name=form.name.data, price=form.price.data, description=form.description.data, image=image)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/addproduct.html', form=form)

@app.route('/admin/order')
def vieworder():
    order = Order.query.all()
    return render_template('order.html',order=order)

@app.route('/admin/order/<order_id>')
def order(order_id):
    order = Order.query.filter_by(id=int(order_id)).first()

    return render_template('admin/vieworder.html', order=order)

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/profile")
def profile():
    return render_template('profile.html')