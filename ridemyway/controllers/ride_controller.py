"""
    Controller for endpoints on rides
"""

from datetime import datetime

from flask import current_app as app

from ridemyway.models.ride import Ride
from ridemyway.utils.response import Response
from ridemyway.utils.validators import date_has_passed


class RideController():
    """
        Controls all CRUD operations of the Ride object.
    """

    def create_ride(self, **kwargs):
        """
            Creates and adds a ride to the app database.

            Returns:
                A success status if success adding ride,
                failed status otherwise.
        """
        ride_ids = [x for x in app.database['Rides']]
        if ride_ids:
            ride_id = max(ride_ids) + 1
        else:
            ride_id = 1
        date_offered = datetime.now().strftime('%b %d %Y %H:%M%p')
        self.new_ride = Ride(
            ride_id=ride_id,
            departure=kwargs['departure'],
            origin=kwargs['origin'],
            destination=kwargs['destination'],
            vehicle_number_plate=kwargs['vehicle_number_plate'],
            capacity=kwargs['capacity'],
            cost=kwargs['cost'],
            date_offered=date_offered,
            availability='available')
        ride = self.new_ride.__dict__
        app.database['Rides'][self.new_ride.ride_id] = ride
        message = 'Ride created successfully'
        attributes = {
            'location': '/rides/' + str(ride['ride_id']),
            'repr': self.new_ride.__repr__()
            }
        response = Response.success(message=message, attributes=attributes)
        return response

    def fetch_one(self, ride_id):
        """
            Fetches a single ride from the app database.

            Returns:
                The requested ride,
                failed status if no such ride exists.
        """
        try:
            one_ride = app.database['Rides'][ride_id]
            self.fetched_ride = {
                'rideId': one_ride['ride_id'],
                'departure': one_ride['departure'],
                'origin': one_ride['origin'],
                'destination': one_ride['destination'],
                'cost': one_ride['cost'],
                'vehicleNumberPlate': one_ride['vehicle_number_plate'],
                'capacity': one_ride['capacity'],
                'dateoffered': one_ride['date_offered']
                }
            message = 'Ride fetched successfully'
            response = Response.success(message=message, data=self.fetched_ride)
            return response, 200
        except KeyError:
            meta = {'errors': 1, 'source': '/rides/' + str(ride_id)}
            message = 'NOT FOUND'
            info = 'That ride doesn\'t exist'
            response = Response.failed(meta=meta,
                                       message=message,
                                       info=info)
            return response, 404

    def fetch_all(self):
        """
            Fetches all available rides from the app database.

            Returns:
                All available rides,
        """
        rides_count = 0
        self.fetched_rides = {}
        message = 'Rides fetched successfully'
        for key, value in app.database['Rides'].items():
            if date_has_passed(value['departure']):
                continue
            rides_count += 1
            self.fetched_rides[key] = {
                'departure': value['departure'],
                'origin': value['origin'],
                'destination': value['destination'],
                'cost': value['cost'],
                'vehicle_number_plate': value['vehicle_number_plate'],
                'capacity': value['capacity'],
                'dateoffered': value['date_offered']
                }
        response = Response.success(message=message,
                                    data=self.fetched_rides,
                                    meta={'rides': rides_count})
        return response
