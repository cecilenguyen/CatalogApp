#!/usr/bin/env python3

# create flask app
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# login imports
from flask import session as login_session
import random, string, requests, httplib2, json
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response


# add database to application
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# GConnect
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# login
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('getCatalog'))
        flash("You are now logged out.")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

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
@app.route('/catalog')
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
        newCategory = Category(name = request.form['name'], user_id=login_session['user_id'])
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
                        description = request.form['description'],
                        user = login_session['user_id'])
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
        # check if current user is the owner
        owner = getUserInfo(category.user_id)
        user = getUserInfo(login_session['user_id'])
        # if logged in user != owner redirect them
        if owner.id != user.id:
            flash ("You do not own this category and cannot delete it.")
            return redirect(url_for('getCatalog'))
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
        # check if current user is the owner
        owner = getUserInfo(item.user_id)
        user = getUserInfo(login_session['user_id'])
        # if logged in user != owner redirect them
        if owner.id != user.id:
            flash ("You do not own this item and cannot delete it.")
            return redirect(url_for('getCatalog'))
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
    # check if current user is the owner
    owner = getUserInfo(category.user_id)
    user = getUserInfo(login_session['user_id'])
    # if logged in user != owner redirect them
    if owner.id != user.id:
        flash ("You do not own this category and cannot edit it.")
        return redirect(url_for('getCatalog'))
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
    # check if current user is the owner
    owner = getUserInfo(item.user_id)
    user = getUserInfo(login_session['user_id'])
    # if logged in user != owner redirect them
    if owner.id != user.id:
        flash ("You do not own this item and cannot edit it.")
        return redirect(url_for('getCatalog'))
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