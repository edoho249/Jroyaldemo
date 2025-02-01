# python imports
import os
import traceback

# installed imports
from flask import Blueprint, request, current_app, jsonify

# local imports
from .. import logger
from ..models import Dish, Order

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
