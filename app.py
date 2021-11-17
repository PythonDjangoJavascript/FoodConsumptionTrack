from flask import Flask, render_template, g, request
import sqlite3


# Define app
app = Flask(__name__)


def connect_db():
    """Connect and return database"""
    sql = sqlite3.connect('/Users/alpha/Dev/Flask/FoodTrack/food_log.db')
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


@app.route('/food', methods=['GET', 'POST'])
def food():
    db = get_db()

    if request.method == 'POST':
        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])

        calories = protein * 4 + carbohydrates * 4 + fat * 9

        db.execute('insert into food (name, protin, carbohydrates, fat, calories) values (?, ?, ?, ?, ?)',
                   [name, protein, carbohydrates, fat, calories])
        db.commit()

    cur = db.execute(
        'select name, protin, carbohydrates, fat, calories from food')
    results = cur.fetchall()

    return render_template('add_food.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
