from flask import render_template, request, redirect, url_for
from flask_googlemaps import Map
from app import app
import restaurants
import groups
import comments
import users
import map


@app.route("/")
def index():
    return redirect("/restaurants")

@app.route("/restaurants", methods=["GET", "POST"])
def show_restaurants():
    all_restaurants=restaurants.get_all_restaurants()

    mymap = map.create_map()

    dropdown = groups.get_all_groups()

    if request.method == "GET":
        return render_template("restaurants.html", restaurants=all_restaurants,
                                                   dropdown=dropdown,
                                                   mymap=mymap)

    users.check_csrf()

    if request.form["action"] == "Hae ryhmää":
        group_id = request.form.get("select_group")
        if group_id == "":
            return render_template("restaurants.html", restaurants=all_restaurants,
                                                       error="Valitse ryhmä.",
                                                       dropdown=dropdown,
                                                       mymap=mymap)
        found_restaurants = restaurants.get_restaurants_in_group(group_id)
    else:
        search_string = request.form["search_string"]
        if len(search_string) < 1 or len(search_string) > 20:
            return render_template("restaurants.html",
                                   restaurants=all_restaurants,
                                   error="Hakusana voi olla 1-20 merkkiä pitkä.",
                                   dropdown=dropdown,
                                   mymap=mymap)
        found_restaurants = restaurants.get_restaurants_by_text(search_string)

    return render_template("restaurants.html", restaurants=all_restaurants,
                                               found_restaurants=found_restaurants,
                                               dropdown=dropdown,
                                               mymap=mymap)

@app.route("/restaurant/<int:id>", methods=["GET", "POST"])
def restaurant(id):
    id, name, avg_stars, description = restaurants.get_restaurant_basic_info(id)
    information = restaurants.get_restaurant_extra_info(id)
    restaurant_comments = restaurants.get_restaurant_comments(id)
    if request.method == "GET":
        return render_template("restaurant.html", id=id,
                                                  name=name,
                                                  stars=avg_stars,
                                                  description=description,
                                                  comments=restaurant_comments,
                                                  information=information)
    
    if request.method == "POST":
        users.check_csrf()
        
        stars = request.form["stars"]
        if stars == None or stars == "":
            return render_template("restaurant.html",
                                   id=id,
                                   name=name,
                                   stars=avg_stars,
                                   description=description,
                                   comments=restaurant_comments,
                                   information=information)

        restaurant_comment = request.form["comment"]
        restaurant_id = id
        user_id = users.user_id()
        comments.add_comment(restaurant_id, user_id, stars, restaurant_comment)
        return redirect(url_for("restaurant", id=restaurant_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("login.html", error="Väärä tunnus tai salasana")
        return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("register.html", error="Tunnuksen tulee olla 3-20 merkkiä")
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", error="Salasanat eivät ole samat")
        if password1 == "":
            return render_template("register.html", error="Salasana on tyhjä")
        if len(password1) < 3:
            return render_template("register.html", error="Salasanan pitää olla vähintään 3 merkkiä pitkä")
        if len(password1) > 50:
            return render_template("register.html", error="Salasana on liian pitkä")
        
        if not users.register(username, password1, 0):
            return render_template("register.html", error="Rekisteröinti ei onnistunut")
        
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")
