import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import data


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


db.drop_all()
db.create_all()

for user_data in data.users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"],
    )

    db.session.add(new_user)
    db.session.commit()

for order_data in data.orders:
    new_order = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"],
    )

    db.session.add(new_order)
    db.session.commit()

for offer_data in data.offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"]
    )

    db.session.add(new_offer)
    db.session.commit()

######пользователи

@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        res = []
        for j in User.query.all():
            res.append(j.to_dict())
        return json.dumps(res), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 201
@app.route("/users/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def user(uid: int):
    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]
        db.session.add(u)
        db.session.commit()
        return "", 204
#######  orders
@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        res_1 = []
        for q in Order.query.all():
            res_1.append(q.to_dict())
        return json.dumps(res_1), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )
        db.session.add(new_order)
        db.session.commit()
        return "", 201
@app.route("/orders/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def order(uid: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        q = Order.query.get(uid)
        db.session.delete(q)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        order_data = request.args
        q = Order.query.get(uid)
        q.first_name = order_data.get('first_name')
        q.name = order_data.get('name')
        q.description = order_data.get('description')
        q.start_date = order_data.get('start_date')
        q.end_date = order_data.get('end_date')
        q.address = order_data.get('address')
        q.price = order_data.get('price')
        q.customer_id = order_data.get('customer_id')
        q.executor_id = order_data.get('executor_id')
        db.session.add(q)
        db.session.commit()
        return "", 204
#######   offers
@app.route("/offers", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res_2 = []
        for f in Offer.query.all():
            res_2.append(f.to_dict())
        return json.dumps(res_2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )
        db.session.add(new_offer)
        db.session.commit()
        return "", 201
@app.route("/offers/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def offer(uid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        f = Offer.query.get(uid)
        db.session.delete(f)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        offer_data = request.args
        f = Offer.query.get(uid)
        f.order_id = offer_data.get("order_id")
        f.executor_id = offer_data.get("executor_id")

        db.session.add(f)
        db.session.commit()
        return "", 204

if __name__ == "__main__":
    app.run()