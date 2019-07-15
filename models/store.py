from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')    # Separated query gets generated for the related object

    """
    With lazy="dynamic", items becomes a SQLAlchemy query. For accessing the items in the store, 
    do this: store.items.all(). '.all()' (only needed when lazy="dynamic") makes query go into the 
    database and retrieve all the items. It is called a "lazy" property because the items are not 
    loaded until to do .all().
    """

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()       # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):                                   # insert + update methods
        db.session.add(self)                                # session - collection of objects for the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

