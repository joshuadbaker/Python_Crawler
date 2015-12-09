from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Crawl(db.Model):
  __tablename__ = 'crawl'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  url = db.Column(db.String())
  crawl_all = db.Column(JSON)
  images = relationship("Image", backref="crawl")

  def __init__(self, name, url):
    self.name = name
    self.url = url

    
  def __repr__(self):
    return '<id {}>'.format(self.id)

class Image(db.Model):
  __tablename__ = 'image'
  id = Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  source = db.Column(db.String())
  image_all = db.Column(JSON)
  crawl_id = Column(db.Integer, ForeignKey('crawl.id'))
  

  def __init__(self, name, source, crawl_id):
    self.name = name
    self.source = source
    self.crawl_id = crawl_id

  def __repr__(self):
    return '<id {}>'.format(self.id)


