from dataclasses import dataclass
import json
import time
from flask import Flask, redirect, render_template, url_for
from werkzeug import exceptions
from instance import IApplicationConfiguration
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from icecream import ic

class Base(DeclarativeBase, MappedAsDataclass):
    pass

db: SQLAlchemy = SQLAlchemy(model_class=Base)


def create_app(config: IApplicationConfiguration, /) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    import Application.error_handlers as errhndl
    app.register_error_handler(exceptions.HTTPException, errhndl.toastify_default_errors)
    app.register_error_handler(exceptions.NotFound, errhndl.handle_notfound_errors)

    db.init_app(app)

    from Application.blueprints.todo import models
    with app.app_context():
        db.create_all()

    from Application.blueprints.todo import bp
    app.register_blueprint(bp)

    @app.get('/')
    def home():
        return redirect( url_for('TODO.getAll'))
        # return render_template('temp.html')

    if app.testing:
        @app.get('/throw_error/<value>')
        def simulate_internal_server_error(value):
            if value == 'single':
                raise Exception('Single arg')
            elif value == 'multi':
                raise Exception(*('Multi arg'.split()))
            elif value == 'none':
                raise Exception()
        
        @app.get('/badrequest')
        def bad_request():
            raise exceptions.BadRequest("Testing BadRequest")
            
    return app


