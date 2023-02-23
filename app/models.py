from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    # userId = db.Column(db.String, nullable=False, unique=True)
    # clientId = db.Column(db.String, nullable=False, unique=True)
    # productId = db.Column(db.String, nullable=False, unique=True)
    amount = db.Column(db.Integer, nullable=False)
    # isDelivered = db.Column(db.Boolean)
    # orderedDate = db.Column(db.String, nullable=False)
    deadline = db.Column(db.String, nullable=False)
    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    isPopular = db.Column(db.Boolean)

    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
# flask db init
# flask db migrate
# flask db upgrade
