from flask import flask
app = Flask(__name__)

# homepage
@app.route('/')
@app.route('/catalog')
def getCatalog():

# get all items for specific category
@app.route('/catalog/<path:category>')
def getCategory(category):

# get single item
@app.route('/catalog/<path:category>/<path:item>')
def getItem(category, item):

####### Add routes #######

# add a category
@app.route('/catalog/addCategory', methods=['GET','POST'])
def addCategory():

# add an item
@app.route('/catalog/addItem', methods=['GET','POST'])
def addItem():

####### Add routes #######

# add a category
@app.route('/catalog/addCategory', methods=['GET','POST'])
def addCategory():

# add an item
@app.route('/catalog/addItem', methods=['GET','POST'])
def addItem():



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)