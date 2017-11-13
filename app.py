#!/usr/bin/env python3

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
@app.route('/catalog/<path:category>/<int:id>')
def getCategory(category, id):
    categories = session.query(Category)
    category = session.query(Category).filter_by(name=category, id=id).first()
    items = session.query(Item).filter_by(category_id = category.id)
    return render_template('items.html', categories=categories, category=category, items=items)

# get single item
@app.route('/catalog/<path:category>/<path:item>/<int:id>')
def getItem(category, item, id):
    item = session.query(Item).filter_by(name=item, id=id).first()
    return render_template('item.html', item=item)

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
        categoryId = session.query(Category).filter_by(name=request.form['category']).first().id
        return redirect(url_for('getCategory', category=request.form['category'], id=categoryId))
    else:
        return render_template('addItem.html', categories=categories)

####### Delete routes #######

# delete a category
@app.route('/catalog/<path:category>/<int:id>/delete', methods=['GET','POST'])
def deleteCategory(category, id):
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=category, id=id).first()
        session.delete(category)
        session.commit()
        # delete all items under that category as well
        items = session.query(Item).filter_by(category_id=id)
        for i in items:
            session.delete(i)
            session.commit()
        flash("Successfully deleted category!")
        return redirect(url_for('getCatalog'))
    else:
        return render_template('deleteItem.html')

# delete an item
@app.route('/catalog/<path:category>/<path:item>/<int:id>/delete', methods=['GET','POST'])
def deleteItem(category, item, id):
    if request.method == 'POST':
        item = session.query(Item).filter_by(name=item, id=id).first()
        session.delete(item)
        session.commit()
        flash("Successfully deleted item!")
        categoryId = session.query(Category).filter_by(name=category).first().id
        return redirect(url_for('getCategory', category=category, id=categoryId))
    else:
        return render_template('deleteItem.html')

####### Edit routes #######
# edit a category
@app.route('/catalog/<path:category>/<int:id>/edit', methods=['GET','POST'])
def editCategory(category, id):
    category = session.query(Category).filter_by(name=category, id=id).first()
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
        session.add(category)
        session.commit()
        flash("Successfully edited category!")
        return redirect(url_for('getCatalog'))
    else:
        return render_template('editCategory.html', category=category)

# edit an item
@app.route('/catalog/<path:category>/<path:item>/<int:id>/edit', methods=['GET','POST'])
def editItem(category, item, id):
    categories = session.query(Category)
    item = session.query(Item).filter_by(name=item, id=id).first()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['category']:
            item.category = session.query(Category).filter_by(name=request.form['category']).first()
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        flash("Successfully edited item!")
        categoryId = session.query(Category).filter_by(name=request.form['category']).first().id
        return redirect(url_for('getCategory', category=request.form['category'], id=categoryId))
    else:
        return render_template('editItem.html', categories=categories, item=item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)