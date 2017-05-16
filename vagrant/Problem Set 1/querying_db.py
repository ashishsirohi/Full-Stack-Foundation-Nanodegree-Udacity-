from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy
engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Query 1
puppies = session.query(Puppy).order_by(Puppy.name)
for puppy in puppies:
	print puppy.name

#Query 2
#puppies = session.query(Puppy).order_by(Puppy.name)

#Query 3
puppies = session.query(Puppy).order_by(Puppy.weight)
for puppy in puppies:
	print puppy.name
	print puppy.weight

#Query 4
puppies = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
for puppy in puppies:
	print puppy[0].id, puppy[0].name, puppy[1]
