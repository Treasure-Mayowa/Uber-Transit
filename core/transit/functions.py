from .models import *
from math import radians, sin, cos, sqrt, atan2

# Non-view functions
def journey(start_lat, start_long, end_lat, end_long):
    if abs(start_lat - end_lat) > 0.100 or abs(end_long - start_long) > 0.001:

        max_distance_km = 2

        transit_within_range = []

        # Convert the user's start latitude and longitude from degrees to radians
        current_latitude_rad = radians(start_lat)
        current_longitude_rad = radians(start_long)

        transit_locations = [i.location for i in Transit.objects.all()]

        for location in transit_locations:

            # Convert the location's latitude and longitude from degrees to radians
            location_latitude_rad = radians(location.latitude)
            location_longitude_rad = radians(location.longitude)

            # Calculate the differences between coordinates
            d_latitude = location_latitude_rad - current_latitude_rad
            d_longitude = location_longitude_rad - current_longitude_rad

            # Use Haversine formula to calculate the distance between the two points
            a = sin(d_latitude / 2) ** 2 + cos(current_latitude_rad) * cos(location_latitude_rad) * sin(d_longitude / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance_km = 6371.01 * c  # Radius of the Earth in kilometers

            # Check if the location is within the specified distance
            if distance_km <= max_distance_km:
                transit_within_range.append(Transit.objects.get(location=location))

        return transit_within_range
    else:
        return []

def nearby_drivers(start_lat, start_long):

    max_distance_km = 2

    drivers_within_range = []

    # Convert the user's start latitude and longitude from degrees to radians
    current_latitude_rad = radians(start_lat)
    current_longitude_rad = radians(start_long)

    transit_locations = [i.user.location for i in Driver.objects.filter(available_seats__gt=0)]

    for location in transit_locations:

        # Convert the driver's location's latitude and longitude from degrees to radians
        location_latitude_rad = radians(location.latitude)
        location_longitude_rad = radians(location.longitude)

        # Calculate the differences between coordinates
        d_latitude = location_latitude_rad - current_latitude_rad
        d_longitude = location_longitude_rad - current_longitude_rad

        # Use Haversine formula to calculate the distance between the two points
        a = sin(d_latitude / 2) ** 2 + cos(current_latitude_rad) * cos(location_latitude_rad) * sin(d_longitude / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = 6371.01 * c  # Radius of the Earth in kilometers

        # Check if the location is within the specified distance
        if distance_km <= max_distance_km:
            drivers_within_range.append(Driver.objects.get(user__location=location))

    return drivers_within_range