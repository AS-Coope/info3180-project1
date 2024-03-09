from . import db

class Property():

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    num_of_bedrooms = db.Column(db.Integer)
    num_of_bathrooms = db.Column(db.Integer)
    location = db.Column(db.String(90))
    price = db.Column(db.DECIMAL(11,2))
    type = db.Column(db.String(50))
    description = db.Column(db.String(200))
    filename = db.Column(db.String(200))