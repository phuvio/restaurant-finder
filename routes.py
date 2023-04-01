
from app import app
from flask import render_template, request, redirect
import restaurants
import groups


@app.route("/")
def index():
    dropdown = groups.get_all_groups()
    return render_template("restaurants.html", restaurants=restaurants.get_all_restaurants(),
                                               dropdown=dropdown)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/restaurants", methods=["GET", "POST"])
def show_restaurants():
    dropdown = groups.get_all_groups()

    if request.method == "GET":
        return render_template("restaurants.html", restaurants=restaurants.get_all_restaurants(),
                                                   dropdown=dropdown)

    if request.form["action"] == "Hae ryhmää":
        group_id = request.form.get("select_group")
        if group_id == "":
            return render_template("restaurants.html", restaurants=restaurants.get_all_restaurants(),
                                                       error="Valitse ryhmä.",
                                                       dropdown=dropdown)
        found_restaurants = restaurants.get_restaurants_in_group(group_id)
    else:
        search_string = request.form["search_string"]
        if len(search_string) < 1 or len(search_string) > 20:
            return render_template("restaurants.html", restaurants=restaurants.get_all_restaurants(),
                                                       error="Hakusana voi olla 1-20 merkkiä pitkä.",
                                                       dropdown=dropdown)
        found_restaurants = restaurants.get_restaurants_by_text(search_string)
        
    return render_template("restaurants.html", restaurants=restaurants.get_all_restaurants(),
                                               found_restaurants=found_restaurants,
                                               dropdown=dropdown)

@app.route("/restaurant/<int:id>")
def restaurant(id):
    id, name, avg_stars, description = restaurants.get_restaurant_basic_info(id)
    information = restaurants.get_restaurant_extra_info(id)
    comments = restaurants.get_restaurant_comments(id)
    return render_template("restaurant.html", id=id,
                                              name=name,
                                              stars=avg_stars,
                                              description=description,
                                              comments=comments,
                                              information=information)