from flask_googlemaps import Map
import restaurants


def create_map():
    all_restaurants = restaurants.get_all_restaurants()

    markers = [{"lat": x.latitude,
                "lng": x.longitude,
                "label": x.name}
                for x in all_restaurants]
    
    mymap = Map(
        identifier="mymap",
        lat=60.169857,
        lng=24.938379,
        markers=markers
    )

    return mymap