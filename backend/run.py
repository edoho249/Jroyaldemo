import os
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT"), host=os.getenv("SERVER_NAME"))
