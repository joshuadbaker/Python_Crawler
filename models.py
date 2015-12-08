from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Crawl(db.Model):
  __tablename__ = 'crawl'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  crawl_all = db.Column(JSON)
  images = relationship("Image")

  def __init__(self, name):
    self.name = name
    self.crawl_all = crawl_all
    self.images = images
    
  def __repr__(self):
    return '<id {}>'.format(self.id)

class Image(db.Model):
  __tablename__ = 'image'
  id = Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  image_all = db.Column(JSON)
  crawl_id = Column(db.Integer, ForeignKey('crawl.id'))
  

  def __init__(self, name, image_all):
    self.name = name
    self.image_all = image_all

  def __repr__(self):
    return '<id {}>'.format(self.id)


