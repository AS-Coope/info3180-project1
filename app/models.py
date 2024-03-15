from . import db

class Property(db.Model):

    __tablename__ = 'property'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    num_of_bedrooms = db.Column(db.Integer)
    num_of_bathrooms = db.Column(db.Integer)
    location = db.Column(db.String(90))
    price = db.Column(db.DECIMAL(11,2))
    type = db.Column(db.String(50))
    description = db.Column(db.String(200))
    filename = db.Column(db.String(200))

    def __init__(self, title, num_of_bedrooms, num_of_bathrooms, location, price, type, description, filename):
        self.title = title
        self.num_of_bedrooms = num_of_bedrooms
        self.num_of_bathrooms = num_of_bathrooms
        self.location = location
        self.price = price
        self.type = type
        self.description = description
        self.filename = filename

    def __repr__(self):
        return '<Property %r>' % self.title