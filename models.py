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
    result_id = Column(db.Integer, ForeignKey('result.id'))


    def __init__(self, name, url, result_id):
        self.name = name
        self.url = url
        self.result_id = result_id

    
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Image(db.Model):
    __tablename__ = 'image'
    id = Column(db.Integer, primary_key=True)
    # name = db.Column(db.String())
    source = db.Column(db.String())
    image_all = db.Column(JSON)
    crawl_id = Column(db.Integer, ForeignKey('crawl.id'))
    result_id = Column(db.Integer, ForeignKey('result.id'))


    def __init__(self, source, crawl_id):
        # self.name = name
        self.source = source
        self.crawl_id = crawl_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Result(db.Model):
    __tablename__ = 'result'
    id = Column(db.Integer, primary_key=True)
    crawls = relationship("Crawl", backref="result")
    images = relationship("Image", backref="result")
    tasks = relationship("Task", backref="result")

class Task(db.Model):
    __tablename__ = 'task'
    id = Column(db.Integer, primary_key=True)
    completed = False
    result_id = Column(db.Integer, ForeignKey('result.id'))
    url = db.Column(db.String())
    job_id = db.Column(db.String())

    def __init__(self, completed, result_id, url, job_id):
        self.completed = False
        self.result_id = result_id
        self.url = url
        self.job_id = job_id

    def __repr__(self):
        return '<id {}>'.format(self.id)



