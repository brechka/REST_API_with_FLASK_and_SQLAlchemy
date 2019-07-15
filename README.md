# REST_API_with_FLASK_and_SQLAlchemy

The REST API built with Python, Flask, Flask-RESTful, and Flask-SQLAlchemy.

REST API lets users register and log in, as well as create stores and items. There are two folders: models 
and resources (with item.py, store.py, and user.py files in both folders) and app.py, db.py, blacklist.py files.

A Model is a representation of what our application deals with internally. Whenever two parts of application 
communicate with one another, they'll do so mainly by using Models.

A Resource is what defines how clients will interact with REST API. In the resource are defined the endpoints 
where clients will have to send requests with required data. Resources use Models to communicate with other parts 
of the application and to interact with the database.


## Requirements

The REST API was created using Python 3.7. To run the APP you need to install the following packages with pip
(better to use virtual environment):

```
pip intall flask
pip install flask_restful
pip install flask_restful_extended
pip install flask_jwt_extended
pip install werkzeug.security
pip intall datetime
```


## Run the APP

The entire application is contained within the app.py file.

```
python app.py
```

## Description

###### [app.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/app.py)

In app.py Flask application is initialized and configured. API resources is also seted up.

###### [db.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/db.py)

Database Python object is created, so other files can import it. All other files import the database variable 
from this file.


###### [models/item.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/models/item.py)

The ItemModel contains a definition of what data application deals with, and ways to interact with that data. 
Essentially it is a class with four properties:

- *id;*
- *name;*
- *price;*
- *store_id.*

Methods in the class can be used to find items by name, save them to the database, or retrieve them. 

###### [models/store.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/models/store.py)

The StoreModel is another definition of data application deals with. It contains two properties:

- *id;*
- *name.*

Because every ItemModel has a store_id property, StoreModels are able to use SQLAlchemy to find the ones 
that have a store_id equal to the StoreModel's id. It can do that by using SQLAlchemy's db.relationship().

###### [models/user.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/models/user.py)

The UserModel contains 3 properties:

- *id;*
- *username;*
- *password.*


###### [resources/item.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/resources/item.py)

The resources/item.py defines an Item and ItemList resources which can be used to retrieve one or multiple items 
at once via the API.

###### [resources/store.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/resources/store.py)

The Store resource defines how users can get, create and delete stores. StoreList resource is defined to retrieve 
all stores in our API.
As we run APP using SQLite, the restriction of creating a store before creating an item does not apply. You could 
give an item a store_id of a store that doesn't exist, and SQLite would accept it. But for fully-fledged database, 
such as PostgreSQL or MySQL, the restriction works, so the id of the store and the store_id of the item must match.

###### [resources/user.py](https://github.com/brechka/REST_API_with_FLASK_and_SQLAlchemy/blob/master/resources/user.py)

These resource defines creating and updating data as well as user authentication, token refresh, log outs, 
and more.

