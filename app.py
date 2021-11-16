from flask import Flask, render_template, g
import sqlite3


# Define app
app = Flask(__name__)


def connect_db():
    """Connect and return database"""
    sql = sqlite3('/Users/alpha/Dev/Flask/FoodTrack/food_log.db')
    # This will change the returns to dictionaries (default is tuple)
    sql.row_factory = sqlite3.Row

    return sql


def get_db():
    """Returns database and add it to g if not already added"""
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()

    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """IT recieces error by defaults"""
    """Teardown app context will ensure calling of this func at the end of
    every routs"""
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/view')
def view():
    return render_template('day.html')


@app.route('/food')
def food():
    return render_template('add_food.html')


if __name__ == '__main__':
    app.run(debug=True)
