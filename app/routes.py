from app import app, db
from app.models import Order
from flask import jsonify, request


@app.route("/all")
def all_users():
    users = db.session.query(User).all()
    every_user = [user.to_dict() for user in users]
    return jsonify(users=every_user)


@app.route('/')
def main_page():
    return "<h1>Hello World</h1>"


@app.route("/update_user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.query(User).get(user_id)
    print(user)
    if user:
        user.name = request.args.get("name")
        user.birthdate = request.args.get('birthdate')
        user.gender = request.args.get('gender')
        user.country = request.args.get('country')
        user.region = request.args.get('region')
        user.phone = request.args.get('phone')
        user.email = request.args.get('email')

        db.session.commit()
        return jsonify(response={"success": "Successfully updated the user."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404


@app.route("/update-name/<int:user_id>", methods=["PATCH"])
def patch(user_id):
    new_name = request.args.get("new_name")
    user = db.session.query(User).get(user_id)
    print(user)
    if user:
        user.name = new_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the user."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404


@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    delete_user = User.query.get(user_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_user)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the user from the API."}), 200

    elif not delete_user:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


@app.route("/add", methods=["POST"])
def add_new_user():
    b = request.files['image']
    print(b)
    # c = request.form.get('image')
    # print(c)
    # run $ flask run  -h 0.0.0.0 -p 8000
    new_user = User(
        image=request.form.get("image"),
        name=request.form.get("name"),
        birthdate=request.form.get("birthdate"),
        gender=request.form.get("gender"),
        country=request.form.get("country"),
        region=request.form.get("region"),
        phone=request.form.get("phone"),
        email=request.form.get("email"),

    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new user."})

######### ORDER CRUD #########
### get all orders
@app.route("/all")
def all_orders():
    orders = db.session.query(Order).all()
    every_order = [order.to_dict() for order in orders]
    return jsonify(orders=every_order)

### create order
@app.route("/add_order", methods=["POST"])
def add_new_order():
    data = request.data
    data = json.loads(data)
    print(data)
    new_order = Order(
        userId=request.form.get("userId"),
        clientId=request.form.get("clientId"),
        productId=request.form.get("clientId"),
        amount=request.form.get("amount"),
        isDelivered=request.form.get("isDelivered"),
        orderedDate=request.form.get("orderedDate"),
        deadline=request.form.get("deadline")
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new user."})

### update PATCH order
@app.route("/update-amount/<int:order_id>", methods=["PATCH"])
def patch(order_id):
    new_amount = request.args.get("new_amount")
    order = db.session.query(Order).get(order_id)
    print(order)
    if order:
        order.amount = new_amount
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the order."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a order with that id was not found in the database."}), 404

### update PUT order
@app.route("/update_order/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = db.session.query(Order).get(order_id)
    print(order)
    if order:
        order.userId = request.args.get("userId")
        order.clientId = request.args.get('clientId')
        order.productId = request.args.get('productId')
        order.amount = request.args.get('amount')
        order.isDelivered = request.args.get('isDelivered')
        order.orderedDate = request.args.get('orderedDate')
        order.deadline = request.args.get('deadline')

        db.session.commit()
        return jsonify(response={"success": "Successfully updated the order."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry an order with that id was not found in the database."}), 404

### delete order
@app.route("/delete/<int:order_id>", methods=["DELETE"])
def delete(order_id):
    delete_order = Order.query.get(order_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_order)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the user from the API."}), 200

    elif not delete_order:
        return jsonify(error={"Not Found": "Sorry an order with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

######### PRODUCT CRUD #########
### get all products
@app.route("/all")
def all_products():
    products = db.session.query(Product).all()
    every_product = [product.to_dict() for product in products]
    return jsonify(products=every_product)

### create product
@app.route("/add_product", methods=["POST"])
def add_new_product():
    data = request.data
    data = json.loads(data)
    print(data)
    new_product = Product(
        name=request.form.get("name"),
        code=request.form.get("code"),
        price=request.form.get("price"),
        amount=request.form.get("amount"),
        quantity=request.form.get("quantity"),
        isPopular=request.form.get("isPopular"),
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new user."})


### update PATCH product
@app.route("/update-name/<int:product_id>", methods=["PATCH"])
def patch(product_id):
    new_name = request.args.get("new_name")
    product = db.session.query(Product).get(product_id)
    print(product)
    if product:
        product.name = new_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the order."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a product with that id was not found in the database."}), 404

### update PUT product
@app.route("/update_product/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = db.session.query(Product).get(product_id)
    print(product)
    if product:
        product.name = request.args.get("name")
        product.code = request.args.get('code')
        product.price = request.args.get('price')
        product.quantity = request.args.get('quantity')
        product.isPopular = request.args.get('isPopular')

        db.session.commit()
        return jsonify(response={"success": "Successfully updated the product."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a product with that id was not found in the database."}), 404

### delete product
@app.route("/delete/<int:product_id>", methods=["DELETE"])
def delete(product_id):
    delete_product = Product.query.get(product_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_product)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the product from the API."}), 200

    elif not delete_order:
        return jsonify(error={"Not Found": "Sorry a product with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

######### CLIENT  CRUD #########
### get all clients
@app.route("/all")
def all_clients():
    clients = db.session.query(Client).all()
    every_client = [client.to_dict() for client in clients]
    return jsonify(clients=every_client)

### create client
@app.route("/add_client", methods=["POST"])
def add_new_client():
    data = request.data
    data = json.loads(data)
    print(data)
    new_client = Client(
        name=request.form.get("name"),
        region=request.form.get("region"),
        phone=request.form.get("phone"),
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new client."})


### update PATCH client
@app.route("/update-name/<int:clientid>", methods=["PATCH"])
def patch(client_id):
    new_name = request.args.get("new_name")
    client = db.session.query(Client).get(client_id)
    print(client)
    if client:
        client.name = new_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the client."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a client with that id was not found in the database."}), 404

### update PUT client
@app.route("/update_client/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    client = db.session.query(Client).get(client_id)
    print(client)
    if client:
        client.name = request.args.get("name")
        client.region = request.args.get('region')
        client.phone = request.args.get('phone')

        db.session.commit()
        return jsonify(response={"success": "Successfully updated the client."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a client with that id was not found in the database."}), 404

### delete client
@app.route("/delete/<int:client_id>", methods=["DELETE"])
def delete(client_id):
    delete_client = Client.query.get(client_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_client)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the client from the API."}), 200

    elif not delete_order:
        return jsonify(error={"Not Found": "Sorry a client with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

@app.route("/search")
def search_user():
    query = request.args.get("query")
    users = User.query.filter(User.name.contains(query)).all()

    if len(users) >= 1:
        return jsonify(users=[user.to_dict() for user in users])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a user at that location."})
