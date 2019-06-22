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
        item = Item.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found.'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400

        data = Item.parser.parse_args()           # put valid args in data

        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500    # Internal server error

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                {"message": "An error occurred inserting te item."}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                {"message": "An error occurred updating te item."}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
