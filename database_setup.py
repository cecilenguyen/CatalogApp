import sys
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    date = Column(DateTime, nullable = False)
    description = Column(String(300), nullable = False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.name,
            'description': self.description
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)