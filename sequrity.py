from user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):                      # process a jwt-token: retrieve an user_id from jwt-token
    user_id = payload['identity']
    return User.find_by_id(user_id)
    
