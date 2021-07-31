
from classflask import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', )"
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)
    description = db.Column(db.String(60))
    image = db.Column(db.String(20))
    orders = db.relationship('Order_Item', backref='product', lazy=True)

    def __repr__(self):

        return f"Product('{self.name}', '{self.price}','{self.description}','{self.image}')"
class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(5))

    first_name = db.Column(db.String(20),  nullable=False)
    last_name = db.Column(db.String(20),  nullable=False)
    phone_number = db.Column(db.Integer,  nullable=False)
    email = db.Column(db.String(50),  nullable=False)
    address = db.Column(db.String(100),  nullable=False)
    city = db.Column(db.String(100),  nullable=False)
    state = db.Column(db.String(20),  nullable=False)
    status = db.Column(db.String(10),  nullable=False)
    payment_type = db.Column(db.String(10),  nullable=False)
    items = db.relationship('Order_Item', backref='order', lazy=True)

    def order_total(self):
        return db.session.query(db.func.sum(Order_Item.quantity * Product.price)).join(Product).filter(Order_Item.order_id == self.id).scalar() + 100
    def quantity_total(self):
        return db.session.query(db.func.sum(Order_Item.quantity)).filter(Order_Item.order_id == self.id).scalar()

class Order_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer,  nullable=False)