from flask import Blueprint, request
from api.models import sql_db, mongo_db
from api.core import create_response, serialize_list

main = Blueprint("main", __name__)  # initialize blueprint


# function that is called when you visit /
@main.route("/")
def index():
    return "<h1>Hello World!</h1>"
