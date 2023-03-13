import json
from datetime import timedelta
from pprint import pprint

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.models import Order, Product, Client
from app.models import User
from flask import jsonify, request
import jwt
from datetime import datetime, timedelta


@app.route("/aaa")
def test():
    return "<h1> hello </h1>"


@app.route("/create_user", methods=["POST"])
def add_new_user():
    try:
        data = request.data.decode('utf8').replace("'", '"')
        myjson = json.loads(data)
        user = {
            'name': myjson["name"],
            'region': myjson["password"],
            'phone': myjson["phone"],
        }
        new_user = User(
            name=myjson["name"],
            password=myjson["password"],
            phone=myjson["phone"],
        )
        db.session.add(new_user)
        db.session.commit()
        token = jwt.encode({
            'username': myjson["name"],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8'), 'user': user}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User already exists', 'status': 400}), 400


### create client
@app.route("/add_client", methods=["POST"])
def add_new_client():
    data = request.data.decode('utf8').replace("'", '"')
    myjson = json.loads(data)
    client = {
        'name': myjson["name"],
        'region': myjson["region"],
        'phone': myjson["phone"],
    }
    new_client = Client(
        name=myjson["name"],
        region=myjson["region"],
        phone=myjson["phone"],
    )
    db.session.add(new_client)
    db.session.commit()
    token = jwt.encode({
        'username': myjson["name"],
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('utf-8'), 'user': client}), 200


@app.route('/sign_in', methods=['POST'])
def login():
    # Get the username and password from the request body
    data = request.data.decode('utf8').replace("'", '"')
    myjson = json.loads(data)
    print(myjson)
    username = myjson['username']
    password = myjson['password']
    matched = User.query.filter_by(name=username, password=password).all()
    all_matched_users = [user.to_dict() for user in matched]
    print(all_matched_users)
    if len(all_matched_users) == 0:
        return jsonify({"message": "User not found, please check your username and password"}), 400
    # Create a JWT token with a 1-hour expiration time

    token = jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, app.config['SECRET_KEY'])
    payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
    print(payload)
    # Return the JWT token
    return jsonify({'token': payload['username'], 'user': all_matched_users}), 200


# dahnuass
### create order
@app.route("/add_order", methods=["POST"])
def add_new_order():
    data = request.data.decode('utf8').replace("'", '"')
    myjson = json.loads(data)
    print(myjson)
    # x = jwt.decode(myjson['userId'], 'secret_key', algorithms=['HS256'])
    print("--------------------------------")
    print(myjson)
    print("--------------------------------")

    new_order = Order(
        amount=myjson["amount"],
        deadline=myjson["deadline"],
        productCode=myjson['productCode'],
        clientName=myjson['clientName'],
        userId=myjson['userId'],
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new order."})


@app.route('/all_orders', methods=['GET'])
def all_orders():
    orders = db.session.query(Order).all()
    every_order = [order.to_dict() for order in orders]
    return jsonify(every_order)


@app.route('/all_orders_for_dashboard', methods=['GET'])
def all_orders_for_dashboard():
    orders = db.session.query(Order).all()
    item_counts = {}
    for item in orders:
        if item.productCode in item_counts:
            item_counts[item.productCode] += 1
        else:
            item_counts[item.productCode] = 1

    # Sort the dictionary in descending order based on the counts of the items
    sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)

    # Calculate the total count of all items
    total_count = sum(item_counts.values())

    # Calculate the total count of the top ten items
    top_ten_count = sum([count for _, count in sorted_items[:10]])

    # Calculate the percentage of the top ten items
    top_ten_percentage = (top_ten_count / total_count) * 100

    print(f"The top ten items represent {top_ten_percentage:.2f}% of the total count.")
    print(f"The top ten items represent {item_counts}")
    return jsonify({"top_sales": item_counts})


@app.route('/all_clients', methods=['GET'])
def all_clients():
    clients = db.session.query(Client).all()
    every_client = [client.to_dict() for client in clients]
    return jsonify(every_client)


# @app.route("/all")
# def all_users():
#     users = db.session.query(User).all()
#     every_user = [user.to_dict() for user in users]
#     return jsonify(users=every_user)
#
#
# @app.route('/')
# def main_page():
#     return "<h1>Hello World</h1>"
#
#
# @app.route("/update_user/<int:user_id>", methods=["PUT"])
# def update_user(user_id):
#     user = db.session.query(User).get(user_id)
#     print(user)
#     if user:
#         user.name = request.args.get("name")
#         user.birthdate = request.args.get('birthdate')
#         user.gender = request.args.get('gender')
#         user.country = request.args.get('country')
#         user.region = request.args.get('region')
#         user.phone = request.args.get('phone')
#         user.email = request.args.get('email')
#
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the user."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404
#
#
# @app.route("/update-name/<int:user_id>", methods=["PATCH"])
# def patch(user_id):
#     new_name = request.args.get("new_name")
#     user = db.session.query(User).get(user_id)
#     print(user)
#     if user:
#         user.name = new_name
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the user."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404
#
#
# # hey
#
# @app.route("/delete/<int:user_id>", methods=["DELETE"])
# def delete(user_id):
#     delete_user = User.query.get(user_id)
#     api_key = request.args.get("api-key")
#     if api_key == "TopSecretAPIKey":
#         db.session.delete(delete_user)
#         db.session.commit()
#         return jsonify(response={"success": "Successfully deleted the user from the API."}), 200
#
#     elif not delete_user:
#         return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404
#
#     else:
#         return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
#


#
# ######### ORDER CRUD #########
# ### get all orders
# @app.route("/all")
# def all_orders():
#     orders = db.session.query(Order).all()
#     every_order = [order.to_dict() for order in orders]
#     return jsonify(orders=every_order)
#
#
# ### create order
# @app.route("/add_order", methods=["POST"])
# def add_new_order():
#     data = request.data
#     data = json.loads(data)
#     print(data)
#     new_order = Order(
#         userId=request.form.get("userId"),
#         clientId=request.form.get("clientId"),
#         productId=request.form.get("clientId"),
#         amount=request.form.get("amount"),
#         isDelivered=request.form.get("isDelivered"),
#         orderedDate=request.form.get("orderedDate"),
#         deadline=request.form.get("deadline")
#     )
#     db.session.add(new_order)
#     db.session.commit()
#     return jsonify(response={"success": "Successfully added the new user."})
#
#
# ### update PATCH order
# @app.route("/update-amount/<int:order_id>", methods=["PATCH"])
# def patch(order_id):
#     new_amount = request.args.get("new_amount")
#     order = db.session.query(Order).get(order_id)
#     print(order)
#     if order:
#         order.amount = new_amount
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the order."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a order with that id was not found in the database."}), 404
#
#
# ### update PUT order
# @app.route("/update_order/<int:order_id>", methods=["PUT"])
# def update_order(order_id):
#     order = db.session.query(Order).get(order_id)
#     print(order)
#     if order:
#         order.userId = request.args.get("userId")
#         order.clientId = request.args.get('clientId')
#         order.productId = request.args.get('productId')
#         order.amount = request.args.get('amount')
#         order.isDelivered = request.args.get('isDelivered')
#         order.orderedDate = request.args.get('orderedDate')
#         order.deadline = request.args.get('deadline')
#
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the order."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry an order with that id was not found in the database."}), 404
#
#
# ### delete order
# @app.route("/delete/<int:order_id>", methods=["DELETE"])
# def delete(order_id):
#     delete_order = Order.query.get(order_id)
#     api_key = request.args.get("api-key")
#     if api_key == "TopSecretAPIKey":
#         db.session.delete(delete_order)
#         db.session.commit()
#         return jsonify(response={"success": "Successfully deleted the user from the API."}), 200
#
#     elif not delete_order:
#         return jsonify(error={"Not Found": "Sorry an order with that id was not found in the database."}), 404
#
#     else:
#         return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
#
#
# ######### PRODUCT CRUD #########
# ### get all products
# @app.route("/all")
# def all_products():
#     products = db.session.query(Product).all()
#     every_product = [product.to_dict() for product in products]
#     return jsonify(products=every_product)
#
#
# ### create product
# @app.route("/add_product", methods=["POST"])
# def add_new_product():
#     data = request.data
#     data = json.loads(data)
#     print(data)
#     new_product = Product(
#         name=request.form.get("name"),
#         code=request.form.get("code"),
#         price=request.form.get("price"),
#         amount=request.form.get("amount"),
#         quantity=request.form.get("quantity"),
#         isPopular=request.form.get("isPopular"),
#     )
#     db.session.add(new_product)
#     db.session.commit()
#     return jsonify(response={"success": "Successfully added the new user."})
#
#
# ### update PATCH product
# @app.route("/update-name/<int:product_id>", methods=["PATCH"])
# def patch(product_id):
#     new_name = request.args.get("new_name")
#     product = db.session.query(Product).get(product_id)
#     print(product)
#     if product:
#         product.name = new_name
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the order."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a product with that id was not found in the database."}), 404
#
#
# ### update PUT product
# @app.route("/update_product/<int:product_id>", methods=["PUT"])
# def update_product(product_id):
#     product = db.session.query(Product).get(product_id)
#     print(product)
#     if product:
#         product.name = request.args.get("name")
#         product.code = request.args.get('code')
#         product.price = request.args.get('price')
#         product.quantity = request.args.get('quantity')
#         product.isPopular = request.args.get('isPopular')
#
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the product."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a product with that id was not found in the database."}), 404
#
#
# ### delete product
# @app.route("/delete/<int:product_id>", methods=["DELETE"])
# def delete(product_id):
#     delete_product = Product.query.get(product_id)
#     api_key = request.args.get("api-key")
#     if api_key == "TopSecretAPIKey":
#         db.session.delete(delete_product)
#         db.session.commit()
#         return jsonify(response={"success": "Successfully deleted the product from the API."}), 200
#
#     elif not delete_product:
#         return jsonify(error={"Not Found": "Sorry a product with that id was not found in the database."}), 404
#
#     else:
#         return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
#

@app.route("/get_client/<int:id>", methods=["GET"])
def client(id):
    get_client = [Client.query.get(id)]
    one_client = [c.to_dict() for c in get_client]
    # api_key = request.args.get("api-key")
    print(one_client)
    return jsonify(one_client)
#
# ######### CLIENT  CRUD #########
# ### get all clients
# @app.route("/all")
# def all_clients():
#     clients = db.session.query(Client).all()
#     every_client = [client.to_dict() for client in clients]
#     return jsonify(clients=every_client)
#
#
# ### create client
# @app.route("/add_client", methods=["POST"])
# def add_new_client():
#     data = request.data
#     data = json.loads(data)
#     print(data)
#     new_client = Client(
#         name=request.form.get("name"),
#         region=request.form.get("region"),
#         phone=request.form.get("phone"),
#     )
#     db.session.add(new_client)
#     db.session.commit()
#     return jsonify(response={"success": "Successfully added the new client."})
#
#
# ### update PATCH client
# @app.route("/update-name/<int:clientid>", methods=["PATCH"])
# def patch(client_id):
#     new_name = request.args.get("new_name")
#     client = db.session.query(Client).get(client_id)
#     print(client)
#     if client:
#         client.name = new_name
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the client."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a client with that id was not found in the database."}), 404
#
#
# ### update PUT client
# @app.route("/update_client/<int:client_id>", methods=["PUT"])
# def update_client(client_id):
#     client = db.session.query(Client).get(client_id)
#     print(client)
#     if client:
#         client.name = request.args.get("name")
#         client.region = request.args.get('region')
#         client.phone = request.args.get('phone')
#
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the client."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a client with that id was not found in the database."}), 404
#
#
# ### delete client
# @app.route("/delete/<int:client_id>", methods=["DELETE"])
# def delete(client_id):
#     delete_client = Client.query.get(client_id)
#     api_key = request.args.get("api-key")
#     if api_key == "TopSecretAPIKey":
#         db.session.delete(delete_client)
#         db.session.commit()
#         return jsonify(response={"success": "Successfully deleted the client from the API."}), 200
#
#     elif not delete_client:
#         return jsonify(error={"Not Found": "Sorry a client with that id was not found in the database."}), 404
#
#     else:
#         return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
#
#
# @app.route("/search")
# def search_user():
#     query = request.args.get("query")
#     users = User.query.filter(User.name.contains(query)).all()
#
#     if len(users) >= 1:
#         return jsonify(users=[user.to_dict() for user in users])
#     else:
#         return jsonify(error={"Not Found": "Sorry, we don't have a user at that location."})
