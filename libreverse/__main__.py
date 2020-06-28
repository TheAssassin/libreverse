from flask_frozen import Freezer
from .app_factory import create_app

app = create_app()
freezer = Freezer(app)

freezer.freeze()
