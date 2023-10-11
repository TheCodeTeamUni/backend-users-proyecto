from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(2), nullable=False)
    token = db.Column(db.String(300))
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime, default=datetime.now())


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.Integer()
    username = fields.String()
    email = fields.String()