from flask_restful import Resource, reqparse       # reqparse used for parsing the request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()           # new object for parsing a request
    parser.add_argument('price',                # parser will look at he JSON payload
                        type=float,
                        required=True,          # no abble to get request without price
                        help='This field cannot be left blank.'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id.'
                        )


    @jwt_required
    # user must provide a valid JWT; work with both Fresh or Non-fresh jwt-token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    @fresh_jwt_required
    # can access only with fresh JWT-token
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400

        # retrieve data from the request body using the parser
        data = Item.parser.parse_args()
        # create a new item
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        # the JWT must have a claim stating that is_admin is True
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']          # price - the only thing is allowed to update
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        # get the JWT; if the user is logged in - return the entire item list,
        # otherwise - return the item names
        user_id = get_jwt_identity()
        # list(map(lambda x: x.json(), ItemModel.query.all()))
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
