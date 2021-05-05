from app import db 
from models.planet import Planet
from flask import request, Blueprint, make_response, jsonify 

planet_bp = Blueprint("planets", __name__, url_prefix="/planets") 

# ENPOINT 1
@planet_bp.route("/add-planet", methods=["POST"])
def add_planet():    
    """Adds a new planet record to the DB table"""
    request_body = request.get_json() 
    new_planet = Planet(
        name=request_body["name"],
        description=request_body["description"], 
        order=request_body["order"] 
    )
    
    db.session.add(new_planet) 
    db.session.commit() 
    return jsonify(f"Planet {new_planet.name} has been successfully added."), 201 # this was not jsonified correctly (/at all)

# ENDPOINT 2 -- added ability to get a planet by title if URL contains a title as a query param 5/5/21
@planet_bp.route("/all-planets", methods=["GET"])
def get_all_planets():
    """Gets data of the existing planets in the DB table"""

    planet_name_from_url = request.args.get("name")
    if planet_name_from_url:
        planets = Planet.query.filter_by(name=planet_name_from_url)
    else:
        planets = Planet.query.all() 
    
    response = [] 
    if planets: 
        for planet in planets:
            response.append({
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "order": planet.order
                })
        return jsonify(response), 200
    if len(response) == 0:
        return jsonify(response), 200
    
    return({"message": "No planets were found."}, 404) 

# ENDPOINT 3 
@planet_bp.route("/<planet_id>", methods=["GET"]) 
def get_one_planet(planet_id):
    """Gets data of a particular planet"""
    planet = Planet.query.get(planet_id)

    if planet:
        return({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "order": planet.order
        }, 200)
    return({"message": f"Planet with id #{planet_id} was not found."}, 404) 

# ENDPOINT 4
@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    """Updates a portion of a single planet's data"""
    planet = Planet.query.get(planet_id)
    
    if planet:
        request_body = request.get_json()
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.order = request_body["order"]

        db.session.commit()
        return ({"message": f"Planet {planet_id} was successfully updated."}, 200)
    return ({"message": f"Planet with id #{planet_id} was not found."}, 404)

# ENDPOINT 5
@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    """Deletes a planet from the database"""
    planet = Planet.query.get(planet_id)

    if planet:
        db.session.delete(planet)
        db.session.commit()
        return ({"message": f"Planet with id {planet_id} has been deleted."}, 200)
    return ({"message": f"Planet with id #{planet_id} was not found."}, 404)