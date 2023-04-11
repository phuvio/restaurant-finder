from flask import render_template, request, redirect, url_for
from app import app
import restaurants
import groups
import comments
import users
import googlemap


regex = '[+-]?[0-9]+\.[0-9]+'

@app.route("/")
def index():
    return redirect("/restaurants")

@app.route("/restaurants", methods=["GET", "POST"])
def show_restaurants():
    mymap = googlemap.create_map()

    dropdown = groups.get_all_groups()

    if request.method == "GET":
        return render_template("restaurants.html",
                               dropdown=dropdown,
                               mymap=mymap)

    if request.form["action"] == "Hae ryhmää":
        group_id = request.form.get("select_group")
        if group_id == "":
            return render_template("restaurants.html",
                                   error="Valitse ryhmä.",
                                   dropdown=dropdown,
                                   mymap=mymap)
        found_restaurants = restaurants.get_restaurants_in_group(group_id)
    else:
        search_string = request.form["search_string"].lower()
        if len(search_string) < 1 or len(search_string) > 20:
            return render_template("restaurants.html",
                                   error="Hakusana voi olla 1-20 merkkiä pitkä.",
                                   dropdown=dropdown,
                                   mymap=mymap)
        found_restaurants = restaurants.get_restaurants_by_text(search_string)

    if not found_restaurants:
        return render_template("restaurants.html",
                               found_restaurants=found_restaurants,
                               dropdown=dropdown,
                               mymap=mymap,
                               error="Ravintoloita ei löytynyt")

    return render_template("restaurants.html",
                           found_restaurants=found_restaurants,
                           dropdown=dropdown,
                           mymap=mymap)

@app.route("/restaurant/<int:id>", methods=["GET", "POST"])
def restaurant(id):
    id, name, avg_stars, description = restaurants.get_restaurant_basic_info(id)
    information = restaurants.get_restaurant_extra_info(id)
    restaurant_comments = restaurants.get_restaurant_comments(id)
    if request.method == "GET":
        return render_template("restaurant.html",
                               id=id,
                               name=name,
                               stars=avg_stars,
                               description=description,
                               comments=restaurant_comments,
                               information=information)

    if request.method == "POST":
        users.check_csrf()

        stars = request.form["stars"]
        if stars is None or stars == "":
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
            return render_template("register.html",
                                   error="Salasanan pitää olla vähintään 3 merkkiä pitkä")
        if len(password1) > 50:
            return render_template("register.html", error="Salasana on liian pitkä")

        if not users.register(username, password1, 0):
            return render_template("register.html", error="Rekisteröinti ei onnistunut")

        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/admin")
def admin():
    users.require_role(0)
    return render_template("admin.html")


@app.route("/add-restaurant", methods=["GET", "POST"])
def add_restaurant():
    users.require_role(0)
    if request.method == "GET":
        return render_template("add-restaurant.html")

    if request.method == "POST":
        users.check_csrf()

        restaurant_name = request.form["restaurant_name"]
        if restaurant_name == "":
            return render_template("add-restaurant.html", error="Ravintolan nimi ei voi olla tyhjä")
        if len(restaurant_name) > 50:
            return render_template("add-restaurant.html", error="Ravintolan nimi on liian pitkä")

        latitude = request.form["latitude"]
        if latitude == "":
            return render_template("add-restaurant.html", error="Leveyspiiri ei voi olla tyhjä")
        try:
            float(latitude)
        except:
            return render_template("add-restaurant.html", error="Leveyspiirin pitää olla numero")
        if not 60 < float(latitude) < 70:
            return render_template("add-restaurant.html",
                                   error="Suomen leveyspiirit ovat 60-70 välillä")

        longitude = request.form["longitude"]
        if longitude == "":
            return render_template("add-restaurant.html", error="Pituuspiiri ei voi olla tyhjä")
        try:
            float(longitude)
        except:
            return render_template("add-restaurant.html", error="Pituuspiirin pitää olla numero")
        if not 22 < float(longitude) < 31:
            return render_template("add-restaurant.html",
                                   error="Suomen pituuspiirit ovat 22-31 välillä")

        description = request.form["description"]
        if len(description) > 500:
            return render_template("add-restaurant.html",
                                   error="Ravintolan esittely on liian pitkä")

        if not restaurants.add_restaurant(restaurant_name, latitude, longitude, description):
            return render_template("add-restaurant.html", error="Tallennus ei onnistunut")

        return render_template("admin.html", message="Tallennus onnistui")

@app.route("/manage-groups", methods=["GET", "POST"])
def manage_groups():
    users.require_role(0)

    dropdown = groups.get_all_groups()
    unvisible = groups.get_all_unvisible_groups()
    if request.method == "GET":
        return render_template("manage-groups.html",
                               dropdown=dropdown,
                               unvisible=unvisible)

    if request.method == "POST":
        users.check_csrf()

        match request.form["action"]:
            case "Hae ryhmää":
                group_id = request.form.get("select_group")
                if group_id == "":
                    return render_template("manage-groups.html",
                                        error="Valitse ryhmä",
                                        dropdown=dropdown,
                                        unvisible=unvisible)

                found_restaurants = restaurants.get_restaurants_in_group_order_by_name(group_id)
                not_in_group_restaurants = restaurants.get_restaurants_not_in_group(group_id)
                return render_template("manage-groups.html",
                                    dropdown=dropdown,
                                    unvisible=unvisible,
                                    found_restaurants=found_restaurants,
                                    not_in_group_restaurants=not_in_group_restaurants,
                                    group_id=group_id)
            case "Poista ryhmä":
                group_id = request.form.get("select_group")
                if group_id == "":
                    return render_template("manage-groups.html",
                                        error="Valitse ryhmä",
                                        dropdown=dropdown,
                                        unvisible=unvisible)
                if not groups.change_group_visibility(group_id, 1):
                    return render_template("manage-groups.html",
                                        error="Tallennus ei onnistunut",
                                        dropdown=dropdown,
                                        unvisible=unvisible)
                dropdown = groups.get_all_groups()
                unvisible = groups.get_all_unvisible_groups()
                return render_template("manage-groups.html",
                                    message="Tallennus onnistui",
                                    dropdown=dropdown,
                                    unvisible=unvisible)
            case "Palauta ryhmä":
                group_id = request.form.get("select_group")
                if group_id == "":
                    return render_template("manage-groups.html",
                                        error="Valitse ryhmä",
                                        dropdown=dropdown,
                                        unvisible=unvisible)
                if not groups.change_group_visibility(group_id, 0):
                    return render_template("manage-groups.html",
                                        error="Tallennus ei onnistunut",
                                        dropdown=dropdown,
                                        unvisible=unvisible)
                dropdown = groups.get_all_groups()
                unvisible = groups.get_all_unvisible_groups()
                return render_template("manage-groups.html",
                                    message="Tallennus onnistui",
                                    dropdown=dropdown,
                                    unvisible=unvisible)
            case "Lisää ryhmään":
                group_id = request.form.get("group_id")
                all_restaurants = restaurants.get_all_restaurants()
                restaurant_id = request.form.get("restaurant_id")
                if not groups.add_restaurant_into_group(group_id, restaurant_id):
                    return render_template("manage-groups.html",
                                        error="Tallennus ei onnistunut",
                                        dropdown=dropdown,
                                        unvisible=unvisible,
                                        found_restaurants=found_restaurants,
                                        all_restaurants=all_restaurants,
                                        group_id=group_id)
                found_restaurants = restaurants.get_restaurants_in_group_order_by_name(group_id)
                not_in_group_restaurants = restaurants.get_restaurants_not_in_group(group_id)
                return render_template("manage-groups.html",
                                    message="Tallennus onnistui",
                                    dropdown=dropdown,
                                    unvisible=unvisible,
                                    found_restaurants=found_restaurants,
                                    not_in_group_restaurants=not_in_group_restaurants,
                                    group_id=group_id)
            case "Poista ryhmästä":
                group_id = request.form.get("group_id")
                restaurant_id = request.form.get("restaurant_id")
                if not groups.remove_restaurant_from_group(group_id, restaurant_id):
                    return render_template("manage-groups.html",
                                        error="Tallennus ei onnistunut",
                                        dropdown=dropdown,
                                        unvisible=unvisible,
                                        found_restaurants=found_restaurants,
                                        all_restaurants=all_restaurants,
                                        group_id=group_id)
                found_restaurants = restaurants.get_restaurants_in_group_order_by_name(group_id)
                not_in_group_restaurants = restaurants.get_restaurants_not_in_group(group_id)
                return render_template("manage-groups.html",
                                    message="Tallennus onnistui",
                                    dropdown=dropdown,
                                    unvisible=unvisible,
                                    found_restaurants=found_restaurants,
                                    not_in_group_restaurants = not_in_group_restaurants,
                                    group_id=group_id)
            case _:
                group_name = request.form["group_name"]
                if group_name == "":
                    return render_template("manage-groups.html",
                                        error="Ryhmän nimi ei voi olla tyhjä",
                                        dropdown=dropdown,
                                        unvisible=unvisible)
                if len(group_name) > 50:
                    return render_template("manage-groups.html",
                                        error="Ryhmän nimi on liian pitkä",
                                        dropdown=dropdown,
                                        unvisible=unvisible)
                if groups.find_group(group_name):
                    return render_template("manage-groups.html",
                                        error="Samanniminen ryhmä on jo olemassa",
                                        dropdown=dropdown,
                                        unvisible=unvisible)

                if not groups.add_group(group_name):
                    return render_template("manage-groups.html",
                                        error="Tallennus ei onnistunut",
                                        dropdown=dropdown,
                                        unvisible=unvisible)
                dropdown = groups.get_all_groups()
                return render_template("manage-groups.html",
                                    message="Tallennus onnistui",
                                    dropdown=dropdown,
                                    unvisible=unvisible)

@app.route("/manage-users", methods=["GET", "POST"])
def manage_users():
    users.require_role(0)

    admin_users = users.get_all_admin_users()
    basic_users = users.get_all_basic_users()

    if request.method == "GET":
        return render_template("manage-users.html",
                               admin_users=admin_users,
                               basic_users=basic_users)

    if request.method == "POST":
        match request.form["action"]:
            case "Poista käyttäjä":
                user_id = request.form.get("select_user")
                if user_id == "":
                    return render_template("manage-users.html",
                                           error="Valitse käyttäjä",
                                           admin_users=admin_users,
                                           basic_users=basic_users)
                if not comments.remove_users_all_comments(user_id):
                    return render_template("manage-users.html",
                                           error="Käyttäjän poistaminen epäonnistui",
                                           admin_users=admin_users,
                                           basic_users=basic_users)
                if not users.remove_user(user_id):
                    return render_template("manage-users.html",
                                           error="Käyttäjän poistaminen epäonnistui",
                                           admin_users=admin_users,
                                           basic_users=basic_users)
                admin_users = users.get_all_admin_users()
                basic_users = users.get_all_basic_users()
                return render_template("manage-users.html",
                                       message="Käyttäjän poistaminen onnistui",
                                       admin_users=admin_users,
                                       basic_users=basic_users)
            case "Muuta perustasolle":
                user_id = request.form.get("admin_id")
                if not users.change_users_role(user_id, 0):
                    return render_template("manage-users.html",
                                           error="Käyttäjän roolin muuttaminen epäonnistui",
                                           admin_users=admin_users,
                                           basic_users=basic_users)
                admin_users = users.get_all_admin_users()
                basic_users = users.get_all_basic_users()
                return render_template("manage-users.html",
                                       admin_users=admin_users,
                                       basic_users=basic_users)
            case "Muuta pääkäyttäjäksi":
                user_id = request.form.get("basic_id")
                if not users.change_users_role(user_id, 1):
                    return render_template("manage-users.html",
                                           error="Käyttäjän roolin muuttaminen epäonnistui",
                                           admin_users=admin_users,
                                           basic_users=basic_users)
                admin_users = users.get_all_admin_users()
                basic_users = users.get_all_basic_users()
                return render_template("manage-users.html",
                                       admin_users=admin_users,
                                       basic_users=basic_users)
  