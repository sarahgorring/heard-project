import os
import time

from flask import Flask
from flask import jsonify
from flask import request

from markupsafe import escape
from collections import defaultdict

from pprint import pprint

from flaskr.db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, Sarah!'

    # @app.route('/user', methods=(["POST"]))
    # def create_user():
    #     name = request.form.get('name')
    #     parent = request.form.get('parent')
    #     tracker_id = request.form.get('parent')
    #     # sql here
    #     return f"user created for {name}"
    #
    #
    # @app.route('/tracker', methods=(["POST"]))
    # def create_tracker():
    #     name = request.form.get('name')
    #     users = request.form.get('users')
    #     return f"tracker created for {name}"

    @app.route('/budget', methods=(['POST']))
    def create_budget():
        name = request.form.get('name')
        user = request.form.get('user_id')
        owner = request.form.get('owner_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        category = request.form.get('category')
        total = request.form.get('total')
        print(name, user, owner, start_date, end_date, category,total)
        db = get_db()
        db.execute(
            "INSERT INTO budget (name, user_id, owner_id, start_date, end_date, category, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, user, owner, start_date, end_date, category, total),
        )
        db.commit()

        return f"budget created for {name}"

    @app.route('/expense', methods=(['POST']))
    def create_expense():
        user = request.form.get('user_id')
        category = request.form.get('category')
        amount = request.form.get('amount')
        expense_date = request.form.get('date')

        if not expense_date:
            expense_date = time.time()

        print(user,category, amount, expense_date)

        db = get_db()
        budget_id = db.execute(
            "SELECT id FROM budget WHERE user_id = ? and category = ? and ? BETWEEN start_date AND end_date",
            (user, category, expense_date),
        ).fetchone()[0]

        db.execute(
            "INSERT INTO expense (user_id, budget_id, category, amount) VALUES (?, ?, ?, ?)",
            (user, budget_id, category, amount),
        )
        db.commit()

        # logic to update budget amount_spent

        return f"expense created for {user}"



    from . import db
    db.init_app(app)

    return app
