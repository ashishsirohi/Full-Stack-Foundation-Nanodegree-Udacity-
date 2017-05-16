from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
"""myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()"""
res = session.query(Restaurant).all()
for r in res:
    print r.name
print "============================"
"""cheesepizza = MenuItem(name="Cheese Pizza", description="Made with all nautral ingredient and fresh mozzarella", course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()"""
items = session.query(MenuItem).all()
for item in items:
    print item.name
