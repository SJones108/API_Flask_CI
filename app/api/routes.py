from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

# Create car
@api.route('/cars', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    car_make = request.json['car_make']
    car_model = request.json['car_model']
    car_year = request.json['car_year']
    car_color = request.json['car_color']
    user_token = current_user_token.token

    car = Car(car_make, car_model, car_year, car_color, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car) 
    return jsonify(response)

# Get car
@api.route('/cars', methods = ['GET'])
@token_required
def retrieve_car(current_user_token):
    a_user = current_user_token.token
    car = Car.query.filter_by(user_token = a_user).all()

    response = cars_schema.dump(car)
    return jsonify(response)

# Get single car
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def retrieve_single_car(current_user_token, id):
    car = Car.query.get(id)

    response = car_schema.dump(car)
    return jsonify(response)

# Update car
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.car_make = request.json['car_make']
    car.car_model = request.json['car_model']
    car.user_token = current_user_token.token

    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Delete car
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)
