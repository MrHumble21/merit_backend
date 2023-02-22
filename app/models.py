from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)



# flask db init
# flask db migrate
# flask db upgrade
