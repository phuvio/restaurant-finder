from flask_googlemaps import Map
import restaurants


def create_map():
    all_restaurants = restaurants.get_all_restaurants()

    markers = []

    for restaurant in all_restaurants:
        marker = {}
        marker["lat"] = restaurant.latitude
        marker["lng"] = restaurant.longitude
        marker["label"] = restaurant.name
        if restaurant.avg_stars:
            link = str(restaurant.avg_stars) + " <a href=/restaurant/" + str(restaurant.id) + ">" + restaurant.name + "</a>"
        else:
            link = "<a href=/restaurant/" + str(restaurant.id) + ">" + restaurant.name + "</a>"
        marker["infobox"] = link
        markers.append(marker)

    mymap = Map(
        identifier="mymap",
        lat=60.169857,
        lng=24.938379,
        markers=markers,
        zoom=14,
        zoom_control=True,
        style="height:400px;width:600px;margin:0;",
    )

    return mymap
