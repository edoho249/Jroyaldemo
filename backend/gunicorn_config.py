import os
from dotenv import load_dotenv

load_dotenv()

# gunicorn config
bind = f"{os.getenv('HOSTNAME')}:{os.getenv('PORT')}"
reload = True
