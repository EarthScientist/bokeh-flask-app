from flask import Flask

app = Flask(__name__)
app.secret_key = 'development key' # this is dangerTown but ok for testing internally
from app import views