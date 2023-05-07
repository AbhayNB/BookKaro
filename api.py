from flask_restful import Resource, Api, fields,marshal_with, reqparse  # for API
from models import *
venue_fields = {
    'venue_id': fields.Integer,
    'name': fields.String,
    'location': fields.String,
    'place': fields.String,
    'capacity': fields.Integer
}

api = Api()
""" Api to show all the shows of perticular venue"""
class VenueShowApi(Resource):
    def get(self, venue_id):
        venue=Venue.query.get(venue_id)
        v=venue.shows
        show_list={a.title:{'price':a.price,'Seats avilable':a.stock,'rating':a.rating,'Release date':a.release_dt} for a in v}
        
        return {'venue_id':venue.venue_id,'name':venue.name,'place':venue.place,'capacity':venue.capacity,'shows':show_list}
""" Api to Show All venues """
class VenuesApi(Resource):
    def get(self):
        ven=Venue.query.all()
        venue_lst={venue.venue_id:{'venue_id':venue.venue_id,'name':venue.name,'place':venue.place,'capacity':venue.capacity,'location':venue.location} for venue in ven}
        return venue_lst

""" API to Show All Shows"""
class ShowsApi(Resource):
    def get(self):
        show=Shows.query.all()
        show_list={a.title:{'price':a.price,'Seats avilable':a.stock,'rating':a.rating,'Release date':a.release_dt} for a in show}
        return show_list


""" Api for CRUD operation of a perticular venue"""
class VenueApi(Resource):
    # GET a venue by ID
    @marshal_with(venue_fields)
    def get(self, venue_id):
        venue = Venue.query.get(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404
        return venue, 200
    
    # CREATE a new venue
    @marshal_with(venue_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the venue is required.')
        parser.add_argument('location', type=str, required=True, help='Location of the venue is required.')
        parser.add_argument('place', type=str, required=True, help='Place of the venue is required.')
        parser.add_argument('capacity', type=int, required=True, help='Capacity of the venue is required.')
        args = parser.parse_args()
        venue = Venue(name=args['name'], location=args['location'], place=args['place'], capacity=args['capacity'])
        db.session.add(venue)
        db.session.commit()
        return venue, 201
    
    # UPDATE an existing venue by ID
    @marshal_with(venue_fields)
    def put(self, venue_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the venue is required.')
        parser.add_argument('location', type=str, required=True, help='Location of the venue is required.')
        parser.add_argument('place', type=str, required=True, help='Place of the venue is required.')
        parser.add_argument('capacity', type=int, required=True, help='Capacity of the venue is required.')
        args = parser.parse_args()

        venue = Venue.query.get(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404
        venue.name = args['name']
        venue.location = args['location']
        venue.place = args['place']
        venue.capacity = args['capacity']
        db.session.commit()
        return venue, 200
    
    # DELETE a venue by ID
    def delete(self, venue_id):
        venue = Venue.query.get(venue_id)
        if not venue:
            return {'message': 'Venue not found'}, 404
        db.session.delete(venue)
        db.session.commit()
        return '', 204

api.add_resource(VenueApi, '/veapi/<int:venue_id>', '/veapi')
api.add_resource(VenueShowApi, '/vsapi/<int:venue_id>')
api.add_resource(VenuesApi, '/vapi')
api.add_resource(ShowsApi, '/sapi')
