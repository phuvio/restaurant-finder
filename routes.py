from flask import render_template, request, redirect, url_for, flash
from app import app
import restaurants
import groups
import comments
import users
import googlemap


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

    if request.method == "POST":
        if request.form["action"] == "Hae ryhmää":
            group_id = request.form.get("select_group")
            if group_id == "":
                flash("Valitse ryhmä", "error")
                return redirect(url_for("show_restaurants"))
            found_restaurants = restaurants.get_restaurants_in_group(group_id)
        else:
            search_string = request.form["search_string"].lower()
            if search_string == "":
                flash("Anna hakusana", "error")
                return redirect(url_for("show_restaurants"))
            if len(search_string) < 1 or len(search_string) > 20:
                flash("Hakusana voi olla 1-20 merkkiä pitkä", "error")
                return redirect(url_for("show_restaurants"))
            found_restaurants = restaurants.get_restaurants_by_text(search_string)

        if not found_restaurants:
            flash("Ravintoloita ei löytynyt", "info")
            return redirect(url_for("show_restaurants"))

        return render_template("restaurants.html",
                            found_restaurants=found_restaurants,
                            dropdown=dropdown,
                            mymap=mymap)

@app.route("/restaurant/<int:res_id>", methods=["GET", "POST"])
def restaurant(res_id):
    res_id, name, avg_stars, description, _, _ = restaurants.get_restaurant_basic_info(res_id)
    information = restaurants.get_restaurant_extra_info(res_id)
    restaurant_comments = restaurants.get_restaurant_comments(res_id)

    if request.method =="GET":
        return render_template("restaurant.html",
                                res_id=res_id,
                                name=name,
                                stars=avg_stars,
                                description=description,
                                comments=restaurant_comments,
                                information=information)

    if request.method == "POST":
        users.check_csrf()

        try:
            stars = request.form["stars"]
        except:
            flash("Anna arvosana klikkaamalla tähtiä", "error")
            return redirect(url_for("restaurant", res_id=res_id))

        restaurant_comment = request.form["comment"]
        user_id = users.user_id()
        if not comments.add_comment(res_id, user_id, stars, restaurant_comment):
            flash("Kommentin tallentaminen epäonnistui", "error")
            return redirect(url_for("restaurant", res_id=res_id))
        return redirect(url_for("restaurant", res_id=res_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            flash("Väärä käyttäjätunnus tai salasana", "error")
            return redirect("/login")
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        errors = [((len(username) < 3 or len(username) > 20),
                  "Käyttäjätunnuksen tulee olla 3-20 merkkiä"),
                  ((password1 == ""), "Salasana on tyhjä"),
                  ((len(password1) < 3), "Salasanan pitää olla vähintään 3 merkkiä pitkä"),
                  ((len(password1) > 50), "Salasana on liian pitkä"),
                  ((password1 != password2), "Salasanat eivät ole samat"),]

        for err in errors:
            if err[0] is True:
                flash(err[1], "error")
                return redirect(url_for("register"))

        if users.get_user_name(username):
            flash("Käyttäjätunnus on jo varattu", "error")
            return redirect(url_for("register"))

        try:
            users.register(username, password1, 0)
        except:
            flash("Rekisteröinti ei onnistunut", "error")
            return render_template("register.html")

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
        latitude = request.form["latitude"]
        try:
            float(latitude)
        except (ValueError, TypeError):
            flash("Leveyspiirin pitää olla numero", "error")
            return redirect(url_for("add_restaurant"))
        longitude = request.form["longitude"]
        try:
            float(longitude)
        except (ValueError, TypeError):
            flash("Pituuspiiriin pitää olla numero", "error")
            return redirect(url_for("add_restaurant"))
        description = request.form["description"]

        errors = [((restaurant_name == ""), "Ravintolan nimi ei voi olla tyhjä"),
                  ((len(restaurant_name) > 50), "Ravintolan nimi on liian pitkä"),
                  ((latitude == ""), "Leveyspiiri ei voi olla tyhjä"),
                  ((not 60 < float(latitude) < 70), "Suomen leveyspiirit ovat 60-70 välillä"),
                  ((longitude == ""), "Pituuspiiri ei voi olla tyhjä"),
                  ((not 22 < float(longitude) < 31), "Suomen pituuspiirit ovat 22-31 välillä"),
                  ((len(description) > 500), "Ravintolan esittely on liian pitkä"),]

        for err in errors:
            if err[0] is True:
                flash(err[1], "error")
                return redirect(url_for("add_restaurant"))
 
        try:
            restaurants.add_restaurant(restaurant_name, latitude, longitude, description)
        except:
            flash("Tallennus ei onnistunut", "error")
            return redirect(url_for("add_restaurant"))

        flash("Tallennus onnistui", "message")
        return redirect(url_for("admin"))

@app.route("/manage-groups", methods=["GET", "POST"])
def manage_groups():
    users.require_role(0)

    dropdown = groups.get_all_groups()
    unvisible = groups.get_all_unvisible_groups()

    if request.method == "GET":
        return render_template("manage-groups.html", dropdown=dropdown, unvisible=unvisible)

    if request.method == "POST":
        users.check_csrf()

        match request.form["action"]:
            case "Hae ryhmää":
                group_id = request.form.get("select_group")
                if group_id == "":
                    flash("Valitse ryhmä", "error")
                    return redirect(url_for("manage_groups"))

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
                    flash("Valitse ryhmä", "error")
                    return redirect(url_for("manage_groups"))

                if not groups.change_group_visibility(group_id, 1):
                    flash("Tallennus ei onnistunut", "error")
                    return redirect(url_for("manage_groups"))

                flash("Tallennus onnistui", "message")
                return redirect(url_for("manage_groups"))

            case "Palauta ryhmä":
                group_id = request.form.get("select_group")
                if group_id == "":
                    flash("Valitse ryhmä", "error")
                    return redirect(url_for("manage_groups"))

                if not groups.change_group_visibility(group_id, 0):
                    flash("Tallennus ei onnistunut", "error")
                    return redirect(url_for("manage_groups"))

                flash("Tallennus onnistui", "message")
                return redirect(url_for("manage_groups"))

            case "Lisää ryhmään":
                group_id = request.form.get("group_id")
                restaurant_id = request.form.get("restaurant_id")
                if not groups.add_restaurant_into_group(group_id, restaurant_id):
                    flash("Tallennus ei onnistunut", "error")
                    return redirect(url_for("manage_groups"))

                found_restaurants = restaurants.get_restaurants_in_group_order_by_name(group_id)
                not_in_group_restaurants = restaurants.get_restaurants_not_in_group(group_id)
                flash("Tallennus onnistui", "message")
                return render_template("manage-groups.html",
                                    dropdown=dropdown,
                                    unvisible=unvisible,
                                    found_restaurants=found_restaurants,
                                    not_in_group_restaurants=not_in_group_restaurants,
                                    group_id=group_id)

            case "Poista ryhmästä":
                group_id = request.form.get("group_id")
                restaurant_id = request.form.get("restaurant_id")
                if not groups.remove_restaurant_from_group(group_id, restaurant_id):
                    flash("Tallennus ei onnistunut", "error")
                    return redirect(url_for("manage_groups"))

                found_restaurants = restaurants.get_restaurants_in_group_order_by_name(group_id)
                not_in_group_restaurants = restaurants.get_restaurants_not_in_group(group_id)
                flash("Tallennus onnistui")
                return render_template("manage-groups.html",
                                    dropdown=dropdown,
                                    unvisible=unvisible,
                                    found_restaurants=found_restaurants,
                                    not_in_group_restaurants = not_in_group_restaurants,
                                    group_id=group_id)

            case _:
                group_name = request.form["group_name"]
                errors = {(group_name == ""): "Ryhmän nimi ei voi olla tyhjä",
                          (len(group_name) > 50): "Ryhmän nimi on liian pitkä",
                          (groups.find_group(group_name)): "Samanniminen ryhmä on jo olemassa",}

                for key, value in errors.items():
                    if key is True:
                        flash(value, "error")
                        return redirect(url_for("manage_groups"))

                if not groups.add_group(group_name):
                    flash("Tallennus ei onnistunut", "error")
                    return redirect(url_for("manage_groups"))

                flash("Tallennus onnistui", "message")
                return redirect(url_for("manage_groups"))

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
        users.check_csrf()

        match request.form["action"]:
            case "Poista käyttäjä":
                user_id = request.form.get("select_user")
                errors = [((user_id == ""), "Valitse käyttäjä"),
                          ((not comments.remove_users_all_comments(user_id)),
                           "Käyttäjän poistaminen epäonnistui"),
                          ((not users.remove_user(user_id)), "Käyttäjän poistaminen epäonnistui"),]

                for err in errors:
                    if err[0] is True:
                        flash(err[1], "error")
                        return redirect(url_for("manage_users"))

                flash("Käyttäjän poistaminen onnistui", "message")
                return redirect(url_for("manage_users"))

            case "Muuta perustasolle":
                user_id = request.form.get("admin_id")
                if not users.change_users_role(user_id, 0):
                    flash("Käyttäjän roolin muuttaminen epäonnistui", "error")
                    return redirect(url_for("manage_users"))

                return redirect(url_for("manage_users"))

            case "Muuta pääkäyttäjäksi":
                user_id = request.form.get("basic_id")
                if not users.change_users_role(user_id, 1):
                    flash("Käyttäjän roolin muuttaminen epäonnistui", "error")
                    return redirect(url_for("manage_users"))

                return redirect(url_for("manage_users"))

@app.route("/manage-restaurants", methods=["GET", "POST"])
def manage_restaurants():
    users.require_role(0)

    visible_restaurants = restaurants.get_all_restaurants()
    hidden_restaurants = restaurants.get_all_hidden_restaurants()

    if request.method == "GET":
        return render_template("manage-restaurants.html",
                               visible_restaurants=visible_restaurants,
                               hidden_restaurants=hidden_restaurants)

    if request.method == "POST":
        match request.form["action"]:
            case "Poista näkyvistä":
                restaurant_id = request.form.get("visible_id")
                if not restaurants.change_restaurant_visibility(restaurant_id, 1):
                    flash("Ravintolan näykyyden muutos epäonnistui", "error")
                    return redirect(url_for("manage_restaurants"))

                return redirect(url_for("manage_restaurants"))

            case "Palauta näkyviin":
                restaurant_id = request.form.get("hidden_id")
                if not restaurants.change_restaurant_visibility(restaurant_id, 0):
                    flash("Ravintolan näykyyden muutos epäonnistui", "error")
                    return redirect(url_for("manage_restaurants"))

                return redirect(url_for("manage_restaurants"))

@app.route("/manage-restaurant/<int:id>", methods=["GET", "POST"])
def manage_restaurant(id):
    users.require_role(0)

    id, name, avg_stars, descr, latitude, longitude = restaurants.get_restaurant_basic_info(id)
    information = restaurants.get_restaurant_extra_info(id)
    restaurant_comments = restaurants.get_restaurant_comments(id)

    if request.method == "GET":
        return render_template("manage-restaurant.html",
                               id=id,
                               name=name,
                               stars=avg_stars,
                               description=descr,
                               latitude=latitude,
                               longitude=longitude,
                               comments=restaurant_comments,
                               information=information)

    if request.method == "POST":
        users.check_csrf()

        match request.form["action"]:
            case "Poista kommentti":
                comment_id = request.form.get("comment_id")
                restaurant_id = request.form.get("restaurant_id")
                if not comments.remove_comment(comment_id):
                    flash("Kommentin poistaminen epäonnistui", "error")
                    return redirect(url_for("manage_restaurant", id=id))

                return redirect(url_for("manage_restaurant",
                                        id=restaurant_id))

            case "Poista lisätieto":
                info_id = request.form.get("info_id")
                if not restaurants.remove_extra_information(info_id):
                    flash("Lisätiedon poistaminen epäonnistui")
                    return redirect(url_for("manage_restaurant", id=id))

                return redirect(url_for("manage_restaurant", id=id))

            case "Lisää lisätieto":
                key = request.form.get("key")
                value = request.form.get("value")

                errors = [((key == ""), "Lisätiedon otsikko ei voi olla tyhjä"),
                          ((len(key) > 50), "Lisätiedon otsikko on liian pitkä"),
                          ((value == ""), "Lisätieto ei voi olla tyhjä"),
                          ((len(value) > 500), "Lisätieto on liian pitkä"),
                          ((not restaurants.add_extra_information(id, key, value)),
                           "Lisätiedon tallennus epäonnistui"),]

                for err in errors:
                    if err[0] is True:
                        flash(err[1], "error")
                        return redirect(url_for("manage_restaurant", id=id))

                return redirect(url_for("manage_restaurant", id=id))

            case "Tallenna tiedot":
                restaurant_id = request.form["restaurant_id"]
                restaurant_name_new = request.form["restaurant_name"]
                latitude_new = request.form["latitude"]
                longitude_new = request.form["longitude"]
                description_new = request.form["description"]
                try:
                    float(latitude_new)
                except (ValueError, TypeError):
                    flash("Leveyspiirin pitää olla numero", "error")
                    return redirect(url_for("manage_restaurant", id=id))
                try:
                    float(longitude_new)
                except (ValueError, TypeError):
                    flash("Pituuspiiriin pitää olla numero")
                    return redirect(url_for("manage_restaurant", id=id))

                errors = [((restaurant_name_new == ""), "Ravintolan nimi ei voi olla tyhjä"),
                          ((len(restaurant_name_new) > 50), "Ravintolan nimi on liian pitkä"),
                          ((latitude_new == ""), "Leveyspiiri ei voi olla tyhjä"),
                          ((not 60 < float(latitude_new) < 70),
                          "Suomen leveyspiirit ovat 60-70 välillä"),
                          ((longitude_new == ""), "Pituuspiiri ei voi olla tyhjä"),
                          ((not 22 < float(longitude_new) < 31),
                          "Suomen pituuspiirit ovat 22-31 välillä"),
                          ((len(description_new) > 500), "Ravintolan esittely on liian pitkä"),
                          (not restaurants.update_restaurant(restaurant_id,
                                                             restaurant_name_new,
                                                             latitude_new,
                                                             longitude_new,
                                                             description_new),
                                                             "Tallennus ei onnistunut")]

                for err in errors:
                    if err[0] is True:
                        flash(err[1], "error")
                        return redirect(url_for("manage_restaurant", id=id))

                flash("Tallennus onnistui", "message")
                return redirect(url_for("manage_restaurant", id=id))
