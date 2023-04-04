from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    favoritePeople = db.relationship('FavoritePeople', backref = 'user', lazy= True )
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)
    mass = db.Column(db.String(120), unique=False, nullable=False)
    skin_Color = db.Column(db.String(120), unique=False, nullable=False)
    eye_Color = db.Column(db.String(120), unique=False, nullable=False)
    birth_year = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    favoritePeople = db.relationship('FavoritePeople', backref = 'people', lazy= True )

    def serialize(self):
        return {
            "id": self.id,        
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "skin_Color": self.skin_Color,
            "eye_Color": self.eye_Color,
            "birth_year": self.birth_year,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    favoritePlanets = db.relationship('FavoritePlanets', backref = 'planets', lazy= True )

    def serialize(self):
        return {
            "id": self.id,        
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "name": self.name
            # do not serialize the password, its a security breach
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_class = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Float, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    favoriteVehicles = db.relationship('FavoriteVehicles', backref = 'vehicles', lazy= True )

    def serialize(self):
        return {
            "id": self.id,        
            "vehicle_class": self.diameter,
            "manufacturer": self.rotation_period,
            "cost_in_credits": self.orbital_period,
            "length": self.gravity,
            "crew": self.population,
            "passengers": self.climate,
            "max_atmosphering_speed": self.terrain,
            "cargo_capacity": self.surface_water,
            "name": self.name
            # do not serialize the password, its a security breach
        }

class FavoritePeople (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable= False)
    
    def serialize(self):
        return {
            "id": self.id,
            "people_id" : people.id,
            "user_id" : user.id
        }

class FavoritePlanets (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable= False)
    
    def serialize(self):
        return {
            "id": self.id,
            "planets_id" : people.id,
            "user_id" : user.id
        }

class FavoriteVehicles (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable= False)
    
    def serialize(self):
        return {
            "id": self.id,
            "vehicles_id" : vehicles.id,
            "user_id" : user.id
        }