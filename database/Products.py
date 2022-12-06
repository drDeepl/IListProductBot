from peewee import *

db = SqliteDatabase('products.db')

class Products(Model):
    name = CharField()
    

    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Products], safe = True)
    db.close()

def db_close():
    db.close()