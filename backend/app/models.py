# python imports
import jwt
import time
import uuid
import traceback
from datetime import datetime

# installed imports
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from app import db, login_manager, logger


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def format_date(self):
        return (
            self.created_at.strftime("%d %b %Y"),
            (
                self.updated_at.strftime("%d %b %Y")
                if self.updated_at
                else self.created_at.strftime("%d %b %Y")
            ),
            None,
        )

    def format_time(self):
        try:
            self.datetime = self.datetime.strftime("%d %b, %Y %I:%M")
        except:
            pass


# db helper functions
class DatabaseHelperMixin(object):
    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, TimestampMixin, UserMixin, DatabaseHelperMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(200), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_no = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date)
    account_type = db.Column(db.String(20), default="regular")
    password_hash = db.Column(db.String(2000), nullable=False)
    orders = db.relationship("Order", backref="user", cascade="delete,all")

    def __init__(
        self,
        firstname: str,
        lastname: str,
        email: str,
        phone_no: str,
        dob: str,
        password=None,
    ) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone_no = phone_no
        self.dob = dob
        self.password_hash = self.get_password_hash(str(password)) if password else None
        self.uid = uuid.uuid4().hex

    def __repr__(self):
        return f"<User: {self.display_name()}>"

    # generate user password i.e. hashing
    def get_password_hash(self, password):
        return generate_password_hash(password)

    # check user password is correct
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # for reseting a user password
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    # return concatenated name
    def display_name(self):
        return f"{self.firstname} {self.lastname}"

    # verify token generated for resetting password
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return None
        return User.query.get(id)


class Dish(db.Model, TimestampMixin, DatabaseHelperMixin):
    __tablename__ = "dish"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    image = db.Column(db.String(256))
    price = db.Column(db.Float, nullable=False)
    popular = db.Column(db.Boolean, default=False)

    def __init__(
        self, name: str, category: str, image: str, price: float, popular: bool = False
    ):
        self.name = name
        self.category = category
        self.image = image
        self.price = price
        self.popular = popular

    def parse(self):
        return {
            "name": self.name,
            "category": self.category,
            "image": self.image,
            "price": self.price,
            "popular": self.popular,
        }

    # get all dish categories
    @staticmethod
    def categories():
        return [
            category[0] for category in db.session.query(Dish.category).distinct().all()
        ]

    # get dishes by category
    @staticmethod
    def dishes_by_category(category=None):
        if category:
            return {
                category: [
                    dish.parse()
                    for dish in Dish.query.filter(Dish.category == category).all()
                ]
            }
        return {cat: Dish.dishes_by_category(cat)[cat] for cat in Dish.categories()}


class Order(db.Model, TimestampMixin, DatabaseHelperMixin):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    dishes = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, dishes: list, user_id: int):
        self.user_id = user_id
        self.dishes = ",".join(
            [
                db.session.query(Dish.id).filter(Dish.name == dish).first()
                for dish in dishes
            ]
        )
        self.price = sum(
            [
                db.session.query(Dish.price).filter(Dish.name == dish).first()
                for dish in dishes
            ]
        )

    def _get_dish_ids(self):
        return [int(dish_id) for dish_id in str(self.dishes).split(",")]

    def get_dishes(self):
        return [Dish.query.get(dish_id).parse() for dish_id in self._get_dish_ids()]
