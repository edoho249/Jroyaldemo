# installed imports
from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.get("/")
def index():
    return render_template("index.html")


@main.get("/menu")
def menu():
    return render_template("menu.html")


@main.get("/order")
def order():
    return render_template("order.html")


@main.get("/gallery")
def gallery():
    return render_template("Gallery.html")


@main.get("/reservation")
def reservation():
    return render_template("Reservation.html")


@main.get("/about")
def about():
    return render_template("about.html")
