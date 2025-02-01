import os
from dotenv import load_dotenv

load_dotenv()

# gunicorn config
bind = f"{os.getenv('HOSTNAME')}:{os.getenv('PORT')}"
reload = True
templates_dir = os.path.join(os.getenv("BASE_DIR"), "frontend", "templates")
reload_extra_files = [
    os.path.abspath(os.path.join(root, file))
    for root, _, files in os.walk(templates_dir)
    for file in files
]
accesslog = os.path.join(os.getenv("LOG_DIR"), "run.log")
errorlog = os.path.join(os.getenv("LOG_DIR"), "run.log")
