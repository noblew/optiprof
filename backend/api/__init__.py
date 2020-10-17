import os

from flask import Flask, request
from flask_cors import CORS

from api.config import config
from api.core import all_exception_handler


# why we use application factories http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app(test_config=None):
    """
    The flask application factory. To run the app somewhere else you can:
    ```
    from api import create_app
    app = create_app()

    if __main__ == "__name__":
        app.run()
    """
    app = Flask(__name__)

    CORS(app)  # add CORS

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    app.config.from_object(config[env])  # config dict is from api/config.py

    # instantiate mongdodb and mysql connection
    from api.models import sql_db, mongo_db

    mongo_db.init_app(app, None, config[env].DBUSER, config[env].DBPASS, sql=False)
    sql_db.init_app(app, config[env].MYSQL_URI, config[env].DBUSER, config[env].DBPASS) 

    # import and register blueprints
    from api.views import main

    # why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    app.register_blueprint(main.main)

    # register error Handler
    app.register_error_handler(Exception, all_exception_handler)

    return app
