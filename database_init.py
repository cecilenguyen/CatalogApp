#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import datetime

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Delete Categories if exisitng.
session.query(Category).delete()
# Delete Items if exisitng.
session.query(Item).delete()
# Delete Users if exisitng.
session.query(User).delete()

# add user
User1 = User(name="John Doe", email="john.doe@gmail.com")
session.add(User1)
session.commit()

defaultUser = session.query(User).filter_by(email="john.doe@gmail.com").first()

# add categories
Category1 = Category(name="Soccer", user=defaultUser)
session.add(Category1)
session.commit()

Category2 = Category(name="Football", user=defaultUser)
session.add(Category2)
session.commit()

Category3 = Category(name="Ice Skating", user=defaultUser)
session.add(Category3)
session.commit()

# add items for soccer
item1 = Item(
	            name="Soccer ball",
	            category_id="1",
	            description="Basic ball for kicking around the field.",
	            user=defaultUser)
session.add(item1)
session.commit()

item2 = Item(
	            name="Cleats",
	            category_id="1",
	            description="Great shoes for running and grip.",
	            user=defaultUser)
session.add(item2)
session.commit()

item3 = Item( 
	            name="Soccer uniform",
	            category_id="1",
	            description="Includes shirt and shorts with team logo and colors.",
	            user=defaultUser)
session.add(item3)
session.commit()

# add items for football
item4 = Item(
	            name="Football",
	            category_id="2",
	            description="Basic football for playing in the backyard or field",
	            user=defaultUser)
session.add(item4)
session.commit()

item5 = Item(
	            name="Jersey",
	            category_id="2",
	            description="Limited edition jersey for local team.",
	            user=defaultUser)
session.add(item5)
session.commit()

item6 = Item(
	            name="Helmet",
	            category_id="2",
	            description="Provides extra head and facial protection for high impact tackles.",
	            user=defaultUser)
session.add(item6)
session.commit()

# add items for ice skating
item7 = Item(
	            name="Skates",
	            category_id="3",
	            description="Razor sharp blades for perfect spins and balance.",
	            user=defaultUser)
session.add(item7)
session.commit()

item8 = Item(
	            name="Leotard",
	            category_id="3",
	            description="Fashionable leotard with skirt with minimal wind resistance and ultimate stretch",
	            user=defaultUser)
session.add(item8)
session.commit()

item9 = Item(
	            name="Jacket",
	            category_id="3",
	            description="Keeps you warm in the rink.",
	            user=defaultUser)
session.add(item9)
session.commit()

print("Database successfully populated!")