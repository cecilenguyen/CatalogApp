from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import datetime

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Delete Categories if exisitng.
session.query(Category).delete()
# Delete Items if exisitng.
session.query(Item).delete()


# add categories
Category1 = Category(id=1, name="Soccer")
session.add(Category1)
session.commit()

Category2 = Category(id=2, name="Football")
session.add(Category2)
session.commit()

Category3 = Category(id=3, name="Ice Skating")
session.add(Category3)
session.commit()

# add items for soccer
item1 = Item(
	            name="Soccer ball",
	            category_id="1",
	            description="Basic ball for kicking around the field.",
	            date=datetime.datetime.now())
session.add(item1)
session.commit()

item2 = Item(
	            name="Cleats",
	            category_id="1",
	            description="Great shoes for running and grip.",
	            date=datetime.datetime.now())
session.add(item2)
session.commit()

item3 = Item( 
	            name="Soccer uniform",
	            category_id="1",
	            description="Includes shirt and shorts with team logo and colors.",
	            date=datetime.datetime.now())
session.add(item3)
session.commit()

# add items for football
item4 = Item(
	            name="Football",
	            category_id="2",
	            description="Basic football for playing in the backyard or field",
	            date=datetime.datetime.now())
session.add(item4)
session.commit()

item5 = Item(
	            name="Jersey",
	            category_id="2",
	            description="Limited edition jersey for local team.",
	            date=datetime.datetime.now())
session.add(item5)
session.commit()

item6 = Item(
	            name="Helmet",
	            category_id="2",
	            description="Provides extra head and facial protection for high impact tackles.",
	            date=datetime.datetime.now())
session.add(item6)
session.commit()

# add items for ice skating
item7 = Item(
	            name="Skates",
	            category_id="3",
	            description="Razor sharp blades for perfect spins and balance.",
	            date=datetime.datetime.now())
session.add(item7)
session.commit()

item8 = Item(
	            name="Leotard",
	            category_id="3",
	            description="Fashionable leotard with skirt with minimal wind resistance and ultimate stretch",
	            date=datetime.datetime.now())
session.add(item8)
session.commit()

item9 = Item(
	            name="Jacket",
	            category_id="3",
	            description="Chill proof jacket for waiting on the sidelines.",
	            date=datetime.datetime.now())
session.add(item9)
session.commit()