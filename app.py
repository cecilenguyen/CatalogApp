# create flask app
from flask import Flask
app = Flask(__name__)

# add database to application
from sqlalchemy import create_engine
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
    output = ''
    for cat in category:
        output += cat.name
        output += '</br>'
        items = session.query(Item).filter_by(category_id = cat.id)
        for i in items:
            output += i.name
            output += '</br>'
        output += '</br>'
    return output
        

# get all items for specific category
@app.route('/catalog/<path:category_name>')
def getCategory(category):
    print()

# get single item
@app.route('/catalog/<path:category>/<path:item>')
def getItem(category, item):
    print()

####### Add routes #######

# add a category
@app.route('/catalog/addCategory', methods=['GET','POST'])
def addCategory():
    print()

# add an item
@app.route('/catalog/addItem', methods=['GET','POST'])
def addItem():
    print()
####### Add routes #######


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)