from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
# use SQLite locally, if DB_URL is not defined
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # SQLAlchemy - main library, has already modif tracker
# allows to return specific messages for errors
app.config['PROPAGATE_EXCEPTIONS'] = True
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_BLACKLIST_ENABLED'] = True
# enabled a blacklist for both access and refresh tokens; no matter what users send, they won't have access
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# can be substituted by app.config['JWT_SECRET_KEY']
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)                       # not creating auth; don't need authenticate & identity func

@jwt.user_claims_loader
# Remember identity is what we define when creating the access token
def add_claims_to_jwt(identity):
    if identity == 1:               # Instead of hard-coding, you chould read from a config file or a database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
# check if a token is blacklisted; it called automatically when blacklist is enabled
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST     # True - if there, False - otherwise

@jwt.expired_token_loader
# notify about access_token expiring; ask to authenticate again
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
# sended token in authorization header is not jwt
# have to keep the argument here, since it's passed in by the caller internally
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
# don't send a jwt at all
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
# send a Non fresh token, but required a fresh one
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
# revoke a token = this token is no longer valid; used for logging out a user
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
