# author: Hoang Ho

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)  # name of running application as argument

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={
                       'check_same_thread': False}, poolclass=StaticPool, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Restaurant 
@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants=restaurants)


@app.route('/restaurants/JSON')
def restaurant():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restau.serialize for restau in restaurants])


@app.route('/restaurants/new', methods=["GET", "POST"])
def newRestaurant():
    if request.method == "POST":
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash(f"New restaurant, {newRestaurant.name} got created!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=["GET", "POST"])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    oldName = restaurant.name
    if request.method == "POST":
        restaurant.name = request.form["name"]
        session.add(restaurant)
        session.commit()
        flash(f"{oldName} get rename to {restaurant.name} got created!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=["GET", "POST"])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    name = restaurantToDelete.name
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash(f"{name} got deleted")
        return redirect(url_for('restaurants'))
    else:
        return render_template(
            'deleteRestaurant.html', restaurant=restaurantToDelete)



@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[item.serialize for item in items])


@app.route('/restaurants/<int:menu_id>/JSON')
def menuItemJSON(menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItems=item.serialize)


@app.route('/restaurants/<int:restaurant_id>/new', methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        newItem.course = request.form["course"]
        newItem.price = request.form["price"]
        newItem.description = request.form["description"]
        session.add(newItem)
        session.commit()
        flash(f"{newItem.name} get created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    itemName = item.name
    if request.method == "POST":
        if request.form['name']:
            item.name = request.form['name']
        session.add(item)
        session.commit()
        flash(f"{itemName} got renamed to {item.name}!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', item=item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    itemName = itemToDelete.name
    if request.method == "POST":
        session.delete(itemToDelete)
        session.commit()
        flash(f"{itemName} got deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
