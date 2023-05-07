import os
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Venue(db.Model):
    venue_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    location=db.Column(db.String(200),nullable=False)
    place=db.Column(db.String(200),nullable=False)
    capacity=db.Column(db.Integer,nullable=False)
    shows=db.relationship("Shows",secondary="venueshow")
    def __repr__(self) -> str:
        return f"{self.venue_id} - {self.name}"
    

class Shows(db.Model):
    show_id= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    image=db.Column(db.String(200),nullable=False,default='logo.png')
    desc=db.Column(db.String(500),nullable=False)
    release_dt=db.Column(db.String(200),nullable=False)
    rating=db.Column(db.Integer,nullable=True)
    price=db.Column(db.Integer,nullable=False)
    tag=db.Column(db.String(200),nullable=False)
    stock=db.Column(db.Integer,nullable=False)
    venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"))
    
    
    def __repr__(self) -> str:
        return f"{self.show_id} - {self.title}"
class VenueShow(db.Model):
    __tablename__='venueshow'
    venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"),primary_key=True)
    show_id= db.Column(db.Integer,db.ForeignKey("shows.show_id"),primary_key=True)
    
class User(db.Model):
    uid= db.Column(db.Integer,primary_key=True)
    Name= db.Column(db.String(200),nullable=False)
    Email= db.Column(db.String(200),nullable=False)
    Pass= db.Column(db.String(200),nullable=False)
    shows=db.relationship("Shows",secondary="show_books")
    venue=db.relationship("Venue",secondary="show_books")
class Admin(db.Model):
    uid= db.Column(db.Integer,primary_key=True)
    Name= db.Column(db.String(200),nullable=False)
    Email= db.Column(db.String(200),nullable=False)
    Pass= db.Column(db.String(200),nullable=False)
    Admin=db.Column(db.String(200),nullable=False,default=True)
class ShowBooks(db.Model):
    uid=db.Column(db.Integer,db.ForeignKey("user.uid"),primary_key=True)
    venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"),primary_key=True)
    show_id= db.Column(db.Integer,db.ForeignKey("shows.show_id"),primary_key=True)
    seats=db.Column(db.Integer,nullable=False)
 