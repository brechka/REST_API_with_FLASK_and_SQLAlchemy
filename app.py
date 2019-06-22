from flask import Flask, request
from flask_restful import Resource, Api, reqparse       # reqparse - for parsing the request
from flask_jwt import JWT, jwt_required

from sequrity import authenticate, identity
from user import UserRegister


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)
""" JWT creates a new endpoint: '/auth' <- send a username and password;
    returns a jwt-token & we send it to the next request we make
    jwt-token itself doesn't do anything; it's a cause of identity func
"""


items = []

class Item(Resource):
    parser = reqparse.RequestParser()           # belongs to class itself; new object for parsing a request
    parser.add_argument('price',                # parser will look at he JSON payload
        type=float,
        required=True,                          # no abble to get request without price
        help='This field cannot be left blank.'
    )

    @jwt_required()                             # at first authenticate, then - get method
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)   # if next doesn't find an item - returns None
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):      # check if we have errors
            return {'message': 'An item with name {} already exists.'.format(name)}, 400

        data = Item.parser.parse_args()         # put valid args in data

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)                  # important to mention debug=True
