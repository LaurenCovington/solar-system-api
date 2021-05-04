# holds test configs
import pytest
from app import create_app
from app import db
from models.planet import Planet 

# set up app
@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

# set up client
@pytest.fixture
def client(app):
    return app.test_client() # simulates testing env

@pytest.fixture
def two_test_planets(app):
    planet1 = Planet(
        id=1,
        name="Test_planet_1", 
        description="Description of Test_planet_1",
        order=100)
    planet2 = Planet(
        id=2,
        name="Test_planet_2", 
        description="Description of Test_planet_2",
        order=200)
    db.session.add_all([planet1, planet2])
    db.session.commit()

@pytest.fixture()
def add_planet(app):
    new_planet = {
        "name": "Test_planet_3", 
        "description": "Description of Test_planet_3",
        "order": 101}
    return new_planet # make sure to a post method func returns something!