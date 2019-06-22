from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from sequrity import authenticate, identity
from user import UserRegister
from item import Item, ItemList


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)
""" JWT creates a new endpoint: '/auth' <- send a username and password;
    returns a jwt-token & we send it to the next request we make
    jwt-token itself doesn't do anything; it's a cause of identity func
"""



api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__name__':
    app.run(port=5000, debug=True)
