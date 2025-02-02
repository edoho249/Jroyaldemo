# python imports
import os
import traceback

# installed imports
from flask import Blueprint, request, current_app, jsonify

# local imports
from .. import logger
from ..models import Dish, Order

from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

api = Blueprint("api", __name__)

#Dishes

@api.post("/add-dish")
def add_dish():
    try:
        data = request.get_json()

        name = data.get("name")
        category = data.get("category")
        image = request.files.get("image")
        price = data.get("price")
        popular = data.get("popular")

        # save dish image
        dish_image_dir = os.path.join(
            current_app.static_folder, "img", "dishes", category
        )
        os.makedirs(dish_image_dir, exist_ok=True)
        image_path = os.path.join(
            dish_image_dir, f"{name}{os.path.splitext(image.filename)[1]}"
        )
        image.save(image_path)

        # create dish record
        dish = Dish(
            name=name, category=category, image=image, price=price, popular=popular
        )
        dish.insert()

        return jsonify(dish.parse())
    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"message": "Error adding dish", "error": str(e)}), 500

@api.post("/update-dish")
def update_dish():
    try:
        data = request.get_json()

        dish_id = data.get("id")  
        name = data.get("name")
        category = data.get("category")
        image = request.files.get("image")
        price = data.get("price")
        popular = data.get("popular")

        dish = Dish.query.get(dish_id)
        if not dish:
            return jsonify({"message": "Dish not found"}), 404

        if name:
            dish.name = name
        if category:
            dish.category = category
        if price:
            dish.price = price
        if popular is not None:
            dish.popular = popular
        if image:
            dish_image_dir = os.path.join(
                current_app.static_folder, "img", "dishes", category
            )
            os.makedirs(dish_image_dir, exist_ok=True)
            image_path = os.path.join(
                dish_image_dir, f"{name}{os.path.splitext(image.filename)[1]}"
            )
            image.save(image_path)

            # Update the dish's image field
            dish.image = image_path
        dish.update()

        return jsonify(dish.parse())

    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"message": "Error updating dish", "error": str(e)}), 500

@api.get("/get-dishes")
def get_dishes():
    try:
        category = request.args.get("category")
        if category:
            dishes = Dish.query.filter(Dish.category == category).all()
        else:
            dishes = Dish.query.all()
        
        return jsonify([dish.parse() for dish in dishes])

    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"message": "Error retrieving dishes", "error": str(e)}), 500
    
def available_tables():
    try:
        # Locking the table records to prevent race condition using SELECT FOR UPDATE
        with db.session.begin():
            available_table = db.session.execute(
                "SELECT table_id FROM orders WHERE table_id BETWEEN 1 AND 30 FOR UPDATE SKIP LOCKED"
            ).fetchone()

            if available_table:
                return available_table.table_id
            return None
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of error
        raise Exception("Database error: " + str(e))

@api.post("/reservations")
def reservations():
    try:
        data = request.get_json()

        duration = data.get("duration")  
        day = data.get("day")  
        time = data.get("time") 

        table_id = available_tables()
        if table_id is None:
            return jsonify({"message": "No tables available."}), 400
        
        start_time_str = f"{day} {time}"
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")

        # Duration is in minutes
        end_time = start_time + timedelta(minutes=duration)

        # Check for reservation overlaps
        existing_reservations = Order.get_all(table_id=table_id)
        for reservation in existing_reservations:
            if (start_time < reservation.end_time and end_time > reservation.start_time):
                return jsonify({"message": "The slot is already reserved."}), 400

        taken_slot = Order(
            table_id=table_id,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            day=day,
            time=time
        )
        taken_slot.insert()

        return jsonify({"message": "Reservation successful", "table_id": table_id, "start_time": start_time, "end_time": end_time})

    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"message": "Error reserving slot", "error": str(e)}), 500