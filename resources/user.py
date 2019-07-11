from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field couldn't be blank"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field couldn't be blank"
                          )


class UserRegister(Resource):                                   # allows users to sign up
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):             # preventing duplicate usernames
            return {'message': 'A user with that username already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201


class User(Resource):
    """
    Retrieve user's details and delete users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):              # analog to authenticate func
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        # this is what 'authenticate()' is used to do
        if user and safe_str_cmp(user.password, data['password']):
            # 'identity=' is what 'identity()' is used to do
            access_token = create_access_token(identity=user.id, fresh=True)        # create a JWT
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"mesage": "Invalid Credentials"}, 401
