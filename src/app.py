"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, FavoritePeople, FavoritePlanets, FavoriteVehicles, TokenBlockedList
#from models import Person

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from datetime import date, time, datetime, timezone, timedelta

from flask_bcrypt import Bcrypt #librería para encriptaciones


app = Flask(__name__)
app.url_map.strict_slashes = False
#Inicio de instancia de Bcrypt
bcrypt = Bcrypt(app)

# Setup the Flask-JWT-Extended extension
#Inicio de instancia de JWT
app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_APP_KEY" ) # Change this!
jwt = JWTManager(app)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()  #<User Antonio>
    users = list(map(lambda item: item.serialize(), users)) #{name:Antonio, password:123, ....} {name:Usuario2, password:123.... }
    print(users)
  
    return jsonify(users), 200


@app.route('/register', methods=['POST'])
def register_user():
    #recibir el body en json, des-jsonificarlo y almacenarlo en la variable body
    body = request.get_json() #request.json() pero hay que importar request y json

    #ordernar cada uno de los campos recibidos
    email = body["email"]
    name = body["name"]
    password = body["password"]
    is_active = body["is_active"]

    #validaciones
    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=400)
    if "email" not in body:
        raise APIException("You need to specify the email", status_code=400)
    #encriptamos el password en la base de datos
    password_encrypted = bcrypt.generate_password_hash(password, 10).decode('utf-8')

    #creada la clase User en la variable new_user
    new_user = User(email=email, name=name, password=password_encrypted, is_active=is_active)

    #comitear la sesión
    db.session.add(new_user) #agregamos el nuevo usuario a la base de datos
    db.session.commit() #guardamos los cambios en la base de datos

    return jsonify({"mensaje":"NewUser Register Correctly"}), 201 

@app.route('/get-user/<int:id>', methods=['GET'])
def get_specific_user(id):
    user = User.query.get(id)    
  
    return jsonify(user.serialize()), 200

@app.route('/get-user', methods=['POST'])
def get_specific_user2():
    body = request.get_json()   
    id = body["id"]

    user = User.query.get(id)   
  
    return jsonify(user.serialize()), 200

@app.route('/get-user', methods=['DELETE'])
def delete_specific_user():
    body = request.get_json()   
    id = body["id"]

    user = User.query.get(id) 

    db.session.delete(user)
    db.session.commit()  
  
    return jsonify("Usuario borrado"), 200

@app.route('/get-user', methods=['PUT'])
def edit_user():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]

    user = User.query.get(id)   
    user.name = name #modifique el nombre del usuario

    db.session.commit()
  
    return jsonify(user.serialize()), 200

#API PEOPLE_______________________________
#API PEOPLE_______________________________
#API PEOPLE_______________________________

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()  #<User Les>
    people = list(map(lambda item: item.serialize(), people)) #{name:Antonio, password:123, ....} {name:Usuario2, password:123.... }
    print(people)
  
    #return jsonify(people), 200
    Poeplebody = {
        "msg": "Ok",
        "people": people
    }

    return jsonify(Poeplebody)

@app.route('/get-people/<int:id>', methods=['GET'])
def get_specific_people(id):
    people = People.query.get(id)    
  
    return jsonify(people.serialize()), 200


@app.route('/post-peolpe', methods=['POST'])
def post_specific_people():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]
    gender = body["gender"]
    eyes_color = body["eyes_color"]
    height = body["height"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=404)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=404)
    if "gender" not in body:
        raise APIException("You need to specify the birthdate", status_code=404)
    if "eyes_color" not in body:
        raise APIException("You need to specify the eyes", status_code=404)
    if "height" not in body:
        raise APIException("You need to specify the height", status_code=404)

    people = People.query.get(id)   
    newCharacter = People(name=name, gender=gender, eyes_color=eyes_color, height=height)

    db.session.add(newCharacter)
    db.session.commit()

    return jsonify(people.serialize()), 200

@app.route('/delete-people', methods=['DELETE'])
def delete_specific_people():
    body = request.get_json()   
    id = body["id"]

    people = People.query.get(id) 

    db.session.delete(people)
    db.session.commit()  
  
    return jsonify("StartWars Character Deleted"), 200

@app.route('/put-people', methods=['PUT'])
def edit_People():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]
    gender = body["gender"]
    eyes_color = body["eyes_color"]
    height = body["height"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=404)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=404)
    if "gender" not in body:
        raise APIException("You need to specify the birthdate", status_code=404)
    if "eyes_color" not in body:
        raise APIException("You need to specify the eyes", status_code=404)
    if "height" not in body:
        raise APIException("You need to specify the height", status_code=404)

    people = People.query.get(id)   
    people.name = name #modifique el nombre del usuario
    people.gender = gender
    people.eyes_color = eyes_color
    people.height = height

    db.session.commit()
  
    return jsonify(people.serialize()), 200


@app.route('/favoritePeople', methods=['POST'])
def add_favorite_pleope():
    body = request.get_json()
    user_id =["user_id"]
    People_id = ["people_id"]

    character = People.query.get(people_id)
    if not character:
        raise APIException('Character Not Found', status_code=404)
    
    user = User.query.get(user_id).first()
    if not user:
        raise APIException('User Not Found', status_code=404)

    fav_exist = favoritePeople.query.filter_by(user_id = user.id, people_id = character.id).first() is not None

    if fav_exist:
        raise APIException('Favorite already exists ', status_code=404)
    
    favorite_people = favoritePeople(user_id = user.id, people_id = character.id)
    db.session.add(favorite_people) #agregamos el nuevo usuario a la base de datos
    db.session.commit()

    return jsonify({
        "people_name":favorite_people.serialize()["people_name"],
        "user": favorite_people.serialize()["user_name"]
    }), 200

@app.route('/removefavoritepeople', methods=['DELETE'])
def remove_favorite_people():
    body = request.get_json()
    user_id = body["user_id"]
    people_id = body["people_id"]

    favorite_people = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()

    if not favorite_people:
        raise APIException('Favorite people not found', status_code=404)

    db.session.delete(favorite_people)
    db.session.commit()

    return jsonify({"msg":"Favorite People removed "}), 200

#API PLANETS_______________________________
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()  #<User Les>
    planets = list(map(lambda item: item.serialize(), planets)) 
    print(planets)
  
    #return jsonify(people), 200
    Planetsbody = {
        "msg": "Done",
        "planets": planets
    }

    return jsonify(Planetsbody)

@app.route('/get-planets/<int:id>', methods=['GET'])
def get_specific_planets(id):
    user = Plantes.query.get(id)    
  
    return jsonify(planets.serialize()), 200


@app.route('/post-planets', methods=['POST'])
def post_specific_planets():
    body = request.get_json()   
    id = body["id"]
    diameter = body["diameter"]
    rotation_period = body["rotation_period"]
    orbital_period = body["orbital_period"]
    gravity = body["gravity"]
    population = body["population"]
    climate = body["climate"]
    terrain = body["terrain"]
    surface_water = body["surface_water"]
    name = body["name"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=404)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=404)
    if "diameter" not in body:
        raise APIException("You need to specify the diameter", status_code=404)
    if "rotation" not in body:
        raise APIException("You need to specify the rotation", status_code=404)
    if "orbital" not in body:
        raise APIException("You need to specify the orbital", status_code=404)
    if "gravity" not in body:
        raise APIException("You need to specify the gravity", status_code=404)
    if "population" not in body:
        raise APIException("You need to specify the population", status_code=404)
    if "climate" not in body:
        raise APIException("You need to specify the climate", status_code=404)
    if "terrain" not in body:
        raise APIException("You need to specify the terrain", status_code=404)
    if "surface_water" not in body:
        raise APIException("You need to specify the surface_water", status_code=404)

    planets = Planets.query.get(id)   
    newPlanet = Planets(surface_water = surface_water, terrain = terrain, climate = climate, population = population, name=name, diameter = diameter, rotation = rotation, orbital = orbital, gravity = gravity)

    db.session.add(newPlanet)
    db.session.commit()

    return jsonify(planet.serialize()), 200

@app.route('/delete-planets', methods=['DELETE'])
def delete_specific_planets():
    body = request.get_json()   
    id = body["id"]

    planets = Planets.query.get(id) 

    db.session.delete(planets)
    db.session.commit()  
  
    return jsonify("StartWars Planet Deleted"), 200

@app.route('/put-planet', methods=['PUT'])
def edit_Planets():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]
    diameter = body["diameter"]
    rotation_period = body["rotation_period"]
    orbital_period = body["orbital_period"]
    gravity = body["gravity"]
    population = body["population"]
    climate = body["climate"]
    terrain = body["terrain"]
    surface_water = body["surface_water"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=404)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=404)
    if "diameter" not in body:
        raise APIException("You need to specify the diameter", status_code=404)
    if "rotation" not in body:
        raise APIException("You need to specify the rotation", status_code=404)
    if "orbital" not in body:
        raise APIException("You need to specify the orbital", status_code=404)
    if "gravity" not in body:
        raise APIException("You need to specify the gravity", status_code=404)
    if "population" not in body:
        raise APIException("You need to specify the population", status_code=404)
    if "climate" not in body:
        raise APIException("You need to specify the climate", status_code=404)
    if "terrain" not in body:
        raise APIException("You need to specify the terrain", status_code=404)
    if "surface_water" not in body:
        raise APIException("You need to specify the surface_water", status_code=404)

    planets = Planets.query.get(id)   
    planets.name = name #modifique el nombre del usuario
    planets.diameter = diameter
    planets.rotation = rotation
    planets.orbital = orbital
    planets.gravity = gravity
    planets.population = population
    planets.climate = climate
    planets.terrain = terrain


    db.session.commit()
  
    return jsonify(planets.serialize()), 200


@app.route('/favoritePlanets', methods=['POST'])
def add_favorite_planets():
    body = request.get_json()
    user_id =["user_id"]
    Planets_id = ["planets_id"]

    planets = Planets.query.get(planets_id)
    if not planets:
        raise APIException('Planet Not Found', status_code=404)
    
    user = User.query.get(user_id).first()
    if not user:
        raise APIException('User Not Found', status_code=404)

    fav_exist = favoritePlanets.query.filter_by(user_id = user.id, planets_id = planets.id).first() is not None

    if fav_exist:
        raise APIException('Favorite already exists ', status_code=404)
    
    favorite_planets = favoritePlanets(user_id = user.id, planets_id = planets.id)
    db.session.add(favorite_planets) #agregamos el nuevo usuario a la base de datos
    db.session.commit()

    return jsonify({"planet_name":favorite_planet.serialize()["planet_name"],
        "user": favorite_planet.serialize()["user_name"]
    }), 201

@app.route('/removefavoriteplanet', methods=['DELETE'])
def remove_favorite_planet():
    body = request.get_json()
    user_id = body["user_id"]
    planet_id = body["planet_id"]

    favorite_planet = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if not favorite_planet:
        raise APIException('Favorite planet not found', status_code=404)

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({"msg":"Favorite planet removed"}), 200

#API VEHICLES_______________________________
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()  #<User Les>
    vehicles = list(map(lambda item: item.serialize(), vehicles)) #{name:Antonio, password:123, ....} {name:Usuario2, password:123.... }
    print(vehicles)
  
    return jsonify(people), 200

@app.route('/get-vehicles/<int:id>', methods=['GET'])
def get_specific_Vehicles(id):
    user = Vehicles.query.get(id)    
  
    #return jsonify(planets.serialize()), 200
    Vehiclesbody = {
        "msg": "Done",
        "vehicles": vehicles
    }

    return jsonify(Vehiclesbody)
    


@app.route('/post-vehicles', methods=['POST'])
def post_specific_Vehicles():
    body = request.get_json()   
    id = body["id"]
    vehicle_class = body["vehicle_class"]
    manufacturer = body["manufacturer"]
    cost_in_credits = body["cost_in_credits"]
    length = body["length"]
    crew = body["crew"]
    passengers = body["passengers"]
    max_atmosphering_speed = body["max_atmosphering_speed"]
    cargo_capacity = body["cargo_capacity"]
    name = body["name"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=404)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=404)
    if "vehicle_class" not in body:
        raise APIException("You need to specify the vehicle_class", status_code=404)
    if "manufacturer" not in body:
        raise APIException("You need to specify the manufacturer", status_code=404)
    if "cost_in_credits" not in body:
        raise APIException("You need to specify the cost_in_credits", status_code=404)
    if "length" not in body:
        raise APIException("You need to specify the length", status_code=404)
    if "crew" not in body:
        raise APIException("You need to specify the crew", status_code=404)
    if "passengers" not in body:
        raise APIException("You need to specify the passengers", status_code=404)
    if "max_atmosphering_speed" not in body:
        raise APIException("You need to specify the max_atmosphering_speed", status_code=404)
    if "cargo_capacity" not in body:
        raise APIException("You need to specify the cargo_capacity", status_code=404)

    vehicles = Vehicles.query.get(id) 
    newVehicle = Vehicles(cargo_capacity = cargo_capacity, max_atmosphering_speed = max_atmosphering_speed, passengers = passengers, crew = crew,length = length, name = name, vehicle_class = vehicle_class, manufacturer = manufacturer, cost_in_credits = cost_in_credits)  
    
    db.session.add(newVehicle)
    db.session.commit() 

    return jsonify(people.serialize()), 200

@app.route('/delete-vehicles', methods=['DELETE'])
def delete_specific_Vehicles():
    body = request.get_json()   
    id = body["id"]

    vehicles = Vehicles.query.get(id) 

    db.session.delete(Vehicles)
    db.session.commit()  
  
    return jsonify("StartWars Vehicle Deleted"), 200

@app.route('/put-vehicles', methods=['PUT'])
def edit_Vehicles():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]
    vehicle_class = body["vehicle_class"]
    manufacturer = body["manufacturer"]
    cost_in_credits = body["cost_in_credits"]
    length = body["length"]
    crew = body["crew"]
    passengers = body["passengers"]
    max_atmosphering_speed = body["max_atmosphering_speed"]
    cargo_capacity = body["cargo_capacity"]
    name = body["name"]

    if body is None:
        raise APIException("You need to specify the request body as json object", status_code=404)
    if "name" not in body:
        raise APIException("You need to specify the name", status_code=404)
    if "vehicle_class" not in body:
        raise APIException("You need to specify the vehicle_class", status_code=404)
    if "manufacturer" not in body:
        raise APIException("You need to specify the manufacturer", status_code=404)
    if "cost_in_credits" not in body:
        raise APIException("You need to specify the cost_in_credits", status_code=404)
    if "length" not in body:
        raise APIException("You need to specify the length", status_code=404)
    if "crew" not in body:
        raise APIException("You need to specify the crew", status_code=404)
    if "passengers" not in body:
        raise APIException("You need to specify the passengers", status_code=404)
    if "max_atmosphering_speed" not in body:
        raise APIException("You need to specify the max_atmosphering_speed", status_code=404)
    if "cargo_capacity" not in body:
        raise APIException("You need to specify the cargo_capacity", status_code=404)

    vehicles = Vehicles.query.get(id)   
    vehicles.name = name #modifique el nombre de la nave
    vehicles.vehicle_class = vehicle_class
    vehicles.manufacturer = manufacturer
    vehicles.cost_in_credits = cost_in_credits
    vehicles.length = length
    vehicles.crew = crew
    vehicles.passengers = passengers
    vehicles.max_atmosphering_speed = max_atmosphering_speed
    vehicles.cargo_capacity = cargo_capacity

    db.session.commit()
  
    return jsonify(vehicles.serialize()), 200

@app.route('/favoriteVehicles', methods=['POST'])
def add_favorite_vehicles():
    body = request.get_json()
    user_id =["user_id"]
    Vehicles_id = ["planets_id"]

    vehicles = Vehicles.query.get(vehicles_id)
    if not vehicles:
        raise APIException('Planet Not Found', status_code=404)
    
    user = User.query.get(user_id).first()
    if not user:
        raise APIException('User Not Found', status_code=404)

    fav_exist = favoriteVehicles.query.filter_by(user_id = user.id, vehicles_id = vehicles.id).first() is not None

    if fav_exist:
        raise APIException('Favorite already exists ', status_code=404)
    
    favorite_vehicles = favoriteVehicles(user_id = user.id, vehicles_id = vehicles.id)
    db.session.add(favorite_vehicles) #agregamos el nuevo usuario a la base de datos
    db.session.commit()

    return jsonify({
        "vehicle_name": favorite_vehicle.serialize()["vehicle_name"],
        "user": favorite_vehicle.serialize()["user_name"]
    }), 201

@app.route('/remove-favorite/vehicle', methods=['DELETE'])
def remove_favorite_vehicle():
    body = request.get_json()
    user_id = body["user_id"]
    vehicle_id = body["vehicle_id"]

    favorite_vehicle = FavoriteVehicles.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()

    if not favorite_vehicle:
        raise APIException('Favorite vehicle not found', status_code=404)

    db.session.delete(favorite_vehicle)
    db.session.commit()

    return jsonify({"msg": "Favorite vehicle removed"}), 200


# Favorites*************************
@app.route('/favorites', methods=['POST'])
@jwt_required()
def list_favorites():
    body = request.get_json()
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        raise APIException('User Not Found', status_code=404)

    favorite_people = list(map(lambda item: item.serialize()["people_name"], FavoritePeople.query.filter_by(user_id=user.id)))
    favorite_planets = list(map(lambda item: item.serialize()["planet_name"], FavoritePlanets.query.filter_by(user_id=user.id)))
    favorite_vehicles = list(map(lambda item: item.serialize()["vehicle_name"], FavoriteVehicles.query.filter_by(user_id=user.id)))

    return jsonify({
        "msg":"ok",
        "all_favorites": favorite_people + favorite_planets + favorite_vehicles,
        "favorite_people": favorite_people,
        "favorite_planets": favorite_planets,
        "favorite_vehicles": favorite_vehicles
    }), 200

@app.route('/favorites/<int:user_id>', methods=['GET'])
@jwt_required()
def get_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)

    favorite_people = list(map(lambda item: item.serialize()["people_name"], FavoritePeople.query.filter_by(user_id=user.id)))
    favorite_planets = list(map(lambda item: item.serialize()["planet_name"], FavoritePlanets.query.filter_by(user_id=user.id)))
    favorite_vehicles = list(map(lambda item: item.serialize()["vehicle_name"], FavoriteVehicles.query.filter_by(user_id=user.id)))

    return jsonify({
        "msg":"ok",
        "all_favorites": favorite_people + favorite_planets + favorite_vehicles,
        "favorite_people": favorite_people,
        "favorite_planets": favorite_planets,
        "favorite_vehicles": favorite_vehicles
    }), 200

# Login*************************


@app.route("/login", methods=["POST"])
def login():
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    userEmailLogin = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"message":"Login failed"}), 401

 #Esta veificaicon es para el inicio de la aplicacion Go all the way Up
    """ if password != user.password:
        return jsonify({"message":"Login failed"}), 401 """
        
 #validar el password encriptado / esto devuelve True si hay coincidencia 
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message":"Login failed"}), 401

# create_access_token() function is used to actually generate the JWT.
    access_token = create_access_token(identity=user.id)
    return jsonify({"token":access_token}), 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    print("UserName:", user.name)
    return jsonify({"Msg":"This is a protected route"}), 200

@app.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"] #Identificador del JWT (es más corto)
    now = datetime.now(timezone.utc) 

    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    tokenBlocked = TokenBlockedList(token=jti , created_at=now, email=user.email)
    db.session.add(tokenBlocked)
    db.session.commit()

    return jsonify({"message":"successfully loggedout "})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)