from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', items=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		old_id = session.query(Restaurant).order_by(Restaurant.id.desc()).first()
		r_id = int(old_id.id)+1
		new_r = Restaurant(name = request.form['name'], id = str(r_id))
		session.add(new_r)
		session.commit()
		flash("New Restaurant Added!!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	itemToEdit = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		itemToEdit.name = request.form['name']
		session.add(itemToEdit)
		session.commit()
		flash("Restaurant has been Edited!!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant_id=restaurant_id, itemToEdit=itemToEdit)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	itemToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Item has been deleted!!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant_id=restaurant_id, itemToDelete=itemToDelete)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem= MenuItem(name=request.form['name'], description=request.form['desc'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))

	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name=request.form['name']
			editedItem.description=request.form['desc']
			editedItem.price=request.form['price']
			editedItem.course=request.form['course']
		session.add(editedItem)
		session.commit()
		flash("Menu Item is Edited!!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, editedItem=editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("Menu Item Deleted!!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)

@app.route('/restaurants/JSON/')
def restaurantsJSON():
    items = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=[item.serialize])

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
