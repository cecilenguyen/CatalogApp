# create flask app
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

# add database to application
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# JSON routes to get all categories and all items
@app.route('/catalog/categories/JSON')
def getCatalogJSON():
    categories = session.query(Category)
    return jsonify(Categories=[cat.serialize for cat in categories])

@app.route('/catalog/items/JSON')
def getItemsJSON():
    items = session.query(Item)
    return jsonify(Items=[i.serialize for i in items])

# homepage
@app.route('/')
@app.route('/catalog/')
def getCatalog():
    category = session.query(Category)
    item = session.query(Item).order_by(desc(Item.date)).limit(5)
    return render_template('homepage.html', category=category, item=item)

# get all items for specific category
@app.route('/catalog/<path:category>')
def getCategory(category):
    categories = session.query(Category)
    category = session.query(Category).filter_by(name=category).first()
    items = session.query(Item).filter_by(category_id = category.id)
    return render_template('items.html', categories=categories, category=category, items=items)

# get single item
@app.route('/catalog/<path:category>/<path:item>')
def getItem(category, item):
    category = session.query(Category).filter_by(name=category).first()
    item = session.query(Item).filter_by(category_id=category.id, name=item).first()
    return render_template('item.html', category=category, item=item)

####### Add routes #######

# add a category
@app.route('/catalog/addCategory', methods=['GET','POST'])
def addCategory():
    if request.method == 'POST':
        newCategory = Category(name = request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("Successfully added category!")
        return redirect(url_for('getCatalog'))
    else:
        return render_template('addCategory.html')

# add an item
@app.route('/catalog/addItem', methods=['GET','POST'])
def addItem():
    categories = session.query(Category)
    if request.method == 'POST':
        newItem = Item(name = request.form['name'],
                        category = session.query(Category).filter_by(name=request.form['category']).first(),
                        description = request.form['description'])
        session.add(newItem)
        session.commit()
        flash("Successfully added item!")
        return redirect(url_for('getCatalog'))
    else:
        return render_template('addItem.html', categories=categories)

####### Delete routes #######
# delete a category
@app.route('/catalog/<path:category>/delete', methods=['GET','POST'])
def deleteCategory(category):
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=category).first()
        session.delete(category)
        session.commit()
        flash("Successfully deleted category!")
        return redirect(url_for('getCatalog'))
    else:
        return render_template('deleteItem.html')

# delete an item
@app.route('/catalog/<path:category>/<path:item>/delete', methods=['GET','POST'])
def deleteItem(category, item):
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=category).first()
        item = session.query(Item).filter_by(category_id=category.id, name=item).first()
        session.delete(item)
        session.commit()
        flash("Successfully deleted item!")
        return redirect(url_for('getCatalog'))
    else:
        return render_template('deleteItem.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)