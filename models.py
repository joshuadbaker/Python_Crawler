from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Crawl(db.Model):
  __tablename__ = 'crawls'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  crawl_all = db.Column(JSON)
  images = relationship("Image")

  def __init__(self, name, images, crawl_all):
    self.name = name
    self.images = images
    self.crawl_all = crawl_all

  def __repr__(self):
    return '<id {}>'.format(self.id)

class Image(db.Model):
  __tablename__ = 'images'

  id = Column(db.Integer, primary_key=True)
  crawl_id = Column(db.Integer, ForeignKey('crawl.id'))
  image_all = db.Column(JSON)

  def __init__(self, crawl_id, image_all):
    self.crawl_id = crawl_id
    self.image_all = image_all

  def __repr__(self):
    return '<id {>'.format(self.id)


