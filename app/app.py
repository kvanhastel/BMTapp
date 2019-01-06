# Entry point for the application.
from app import app, db
from app.models import Gebruiker, Speler, Ploeg
# from app import routes  # For import side-effects of setting up routes.