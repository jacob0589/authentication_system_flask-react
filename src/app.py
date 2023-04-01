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
from models import db, User, People, Planets, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

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

    #creada la clase User en la variable new_user
    new_user = User(email=email, name=name, password=password, is_active=is_active)

    #comitear la sesión
    db.session.add(new_user) #agregamos el nuevo usuario a la base de datos
    db.session.commit() #guardamos los cambios en la base de datos

    return jsonify({"mensaje":"Usuario creado correctamente"}), 201 

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
@app.route('/get-people/<int:id>', methods=['GET'])
def get_specific_people(id):
    user = People.query.get(id)    
  
    return jsonify(people.serialize()), 200


@app.route('/post-peolpe', methods=['POST'])
def post_specific_people():
    body = request.get_json()   
    id = body["id"]

    people = People.query.get(id)   
  
    return jsonify(people.serialize()), 200

@app.route('/delete-people', methods=['DELETE'])
def delete_specific_people():
    body = request.get_json()   
    id = body["id"]

    people = People.query.get(id) 

    db.session.delete(people)
    db.session.commit()  
  
    return jsonify("StartWars Character Deleted"), 200

@app.route('/put-user', methods=['PUT'])
def edit_People():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]

    people = People.query.get(id)   
    people.name = name #modifique el nombre del usuario

    db.session.commit()
  
    return jsonify(people.serialize()), 200

#API PLANETS_______________________________

@app.route('/get-planets/<int:id>', methods=['GET'])
def get_specific_planets(id):
    user = Plantes.query.get(id)    
  
    return jsonify(planets.serialize()), 200


@app.route('/post-planets', methods=['POST'])
def post_specific_planets():
    body = request.get_json()   
    id = body["id"]

    planets = Planets.query.get(id)   
  
    return jsonify(people.serialize()), 200

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

    planets = Planets.query.get(id)   
    planets.name = name #modifique el nombre del usuario

    db.session.commit()
  
    return jsonify(planets.serialize()), 200

#API VEHICLES_______________________________

@app.route('/get-vehicles/<int:id>', methods=['GET'])
def get_specific_Vehicles(id):
    user = Vehicles.query.get(id)    
  
    return jsonify(planets.serialize()), 200


@app.route('/post-vehicles', methods=['POST'])
def post_specific_Vehicles():
    body = request.get_json()   
    id = body["id"]

    vehicles = Vehicles.query.get(id)   
  
    return jsonify(people.serialize()), 200

@app.route('/delete-vehicles', methods=['DELETE'])
def delete_specific_Vehicles():
    body = request.get_json()   
    id = body["id"]

    vehicles = Vehicles.query.get(id) 

    db.session.delete(Vehicles)
    db.session.commit()  
  
    return jsonify("StartWars Planet Deleted"), 200

@app.route('/put-vehicles', methods=['PUT'])
def edit_Vehicles():
    body = request.get_json()   
    id = body["id"]
    name = body["name"]

    vehicles = Vehicles.query.get(id)   
    vehicles.name = name #modifique el nombre del usuario

    db.session.commit()
  
    return jsonify(vehicles.serialize()), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)