from app import app, db
from app.models import User
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
    # c = request.form.get('image')
    # print(c)
    # run $ flask run  -h 0.0.0.0 -p 8000
    new_user = User(
        name=request.form.get("name"),
        region=request.form.get("region"),
        phone=request.form.get("phone"),

    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new user."})


@app.route("/search")
def search_user():
    query = request.args.get("query")
    users = User.query.filter(User.name.contains(query)).all()

    if len(users) >= 1:
        return jsonify(users=[user.to_dict() for user in users])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a user at that location."})
