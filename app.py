# create flask app
from flask import Flask, render_template
app = Flask(__name__)

# add database to application
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# homepage
@app.route('/')
@app.route('/catalog')
def getCatalog():
    category = session.query(Category)
    item = session.query(Item).order_by(desc(Item.date)).limit(5)
    return render_template('homepage.html', category=category, item=item)

# get all items for specific category
@app.route('/catalog/<path:category>')
def getCategory(category):
    category = session.query(Category).filter_by(name=category).first()
    items = session.query(Item).filter_by(category_id = category.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
    return output
    

# get single item
@app.route('/catalog/<path:category>/<path:item>')
def getItem(category, item):
    category = session.query(Category).filter_by(name=category).first()
    item = session.query(Item).filter_by(category_id=category.id, name=item).first()
    output = ''
    output += item.name + '</br>'
    output += item.description
    return output


####### Add routes #######

# add a category
@app.route('/catalog/addCategory', methods=['GET','POST'])
def addCategory():
    print()
    # category = Category(id=1, name="Soccer")
    # session.add(category)
    # session.commit()

# add an item
@app.route('/catalog/addItem', methods=['GET','POST'])
def addItem():
    print()
    # item5 = Item(
    #             name="Jersey",
    #             category_id="2",
    #             description="Limited edition jersey for local team.",
    #             date=datetime.datetime.now())
    # session.add(item5)
    # session.commit()
####### Add routes #######


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)