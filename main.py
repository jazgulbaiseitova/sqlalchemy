from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

DATABASE_URL = "postgresql://zhazgul:1@localhost/product_items"
#"postgresql://username:password@host/db_name"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

ItemPydantic = sqlalchemy_to_pydantic(Item, exclude=["id"])

db_item = ItemPydantic(name='item 3', description='desc lesk', price=190)

def create_item(db_item: ItemPydantic):
    db_item = Item(**db_item.dict())
    with SessionLocal() as db:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        # print(db.query(Item).all())
    return db_item
# create_item(db_item)

def get_item():
    result = []
    with SessionLocal() as db:
        items = db.query(Item).all()
        for item in items:
            result.append({'id': item.id,
                'name':item.name, 
                            'description':item.description,
                            'price':item.price})
    return result
def retrieve_item(id_):
    with SessionLocal() as db:
        item = db.query(Item).filter_by(id=id_).first()
    return item.name, item.description , item.price
print(retrieve_item(3))

def update_item(id_, name_, description_, price_):
    with SessionLocal() as db:
        db.query(Item).filter_by(id=id_).update({'name':name_, 'description':description_, 'price':price_}) 
        db.commit()
        item = db.query(Item).filter_by(id=id_).first()
        return item  

def delete_item(id_):
    with SessionLocal() as db:
        db.query(Item).filter_by(id=id_).delete()
        db.commit()


delete_item(1) 
# update_item(1, 'Jazgul', 'info', 125)
print(get_item())
# retrieve - poisk po id
# update
# delete 


#API


