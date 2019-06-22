import sqlite3
from flask_restful import Resource, reqparse       # reqparse - for parsing the request
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()           # belongs to class itself; new object for parsing a request
    parser.add_argument('price',                # parser will look at he JSON payload
        type=float,
        required=True,                          # no abble to get request without price
        help='This field cannot be left blank.'
    )

    @jwt_required()                             # at first authenticate, then - get method
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found.'}, 404

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
