#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(only=("id", "name", "address")) for restaurant in restaurants]), 200

@app.route("/restaurants/<int:id>", methods=["GET", "DELETE"])
def restaurant_details(id):
    restaurant = db.session.get(Restaurant, id)
    if request.method == "GET":
        if restaurant:
            return jsonify(restaurant.to_dict()), 200
        return jsonify({"error": "Restaurant not found"}), 404

    if request.method == "DELETE":
       if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204
    return jsonify({"error": "Restaurant not found"}), 404
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(only=("id", "name", "ingredients")) for pizza in pizzas]), 200

# Create new restaurant pizza
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        new_restaurant_pizza = RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"]
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)