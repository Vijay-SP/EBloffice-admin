from flask import Flask, session, redirect, request, render_template, url_for
import json
from check_login import check_login
from firebase_crud import *
from cloudinary_crud import *

app = Flask(__name__)
app.secret_key = "ebl_offices_admin_panel_website"

with open("config.json", "r") as c:
    params = json.load(c)['params']


@app.route("/", methods=["GET", "POST"])
def login():
    # if user is logged in
    if ('user' in session and session['user'] == params['admin_user']):
        return redirect("/properties")

    # If user requests to log in
    if request.method == "POST":
        # Redirect to Admin Panel
        username = request.form.get('uname')
        userpassword = request.form.get('pass')
        if (username == params['admin_user'] and userpassword == params['admin_password']):
            session['user'] = username
            return redirect("/properties")

    return render_template("login.html", params=params)


@app.route("/properties")
@check_login
def properties():
    propertiesData = fetchProperties()
    return render_template("properties.html", params=params, properties=propertiesData, active="properties")


@app.route("/brokers")
@check_login
def brokers():
    brokersData = fetchBrokers()
    return render_template("brokers.html", params=params, brokers=brokersData,  active="brokers")


@app.route("/buyers")
@check_login
def buyers():
    usersData = fetchBuyers()
    return render_template("buyers.html", params=params, users=usersData,  active="buyers")

@app.route("/contacts")
@check_login
def contacts():
    contacts = fetchContacts()
    return render_template("contacts.html", params=params, contacts=contacts,  active="contacts")

@app.route("/appointment")
@check_login
def appointments():
    appoints = fetchAppointments()
    return render_template("appointments.html", params=params, appoints=appoints,  active="appointment")

@app.route("/logout")
def logout():
    session.pop('user')
    session.clear()
    return redirect("/")


@app.route("/addproperty", methods=["GET", "POST"])
@check_login
def addproperty():
    # when add button is pressed
    if request.method == "POST":
        # upload the images
        img_url_list = uploadPropertyImages(request)
        floor_plan_list = []
        # check for new floor plan images
        floor_imgs = request.files.getlist("floor-plan-files[]")
        if any(f for f in floor_imgs):
            for link in uploadFloorPlanImages(request):
                floor_plan_list.append(link)

        # upload the data to firebase
        uploadPropertyData(request, img_url_list, floor_plan_list)
        return redirect("/properties")

    return render_template("add_property.html", params=params, active="properties")


@app.route("/property/<id>", methods=["GET", "POST"])
@check_login
def property(id):
    property = fetchProperty(id)

    if request.method == "POST":
        img_links = property["img_links"]
        floor_plans = property["floor_plans"]

        # check for new property images
        prop_imgs = request.files.getlist("prop-files[]")
        if any(f for f in prop_imgs):
            print("Property Image found")
            for link in uploadPropertyImages(request):
                img_links.append(link)

        # check for new floor plan images
        floor_imgs = request.files.getlist("floor-plan-files[]")
        if any(f for f in floor_imgs):
            print("Floor Image found")
            for link in uploadFloorPlanImages(request):
                floor_plans.append(link)

        updateEditedProperty(request, id, img_links, floor_plans)
        return redirect("/properties")

    return render_template("edit_property.html", params=params, property=property, active="properties")


@app.route("/delete/<id>", methods=["GET", "POST"])
@check_login
def deleteProperty(id):
    property = fetchProperty(id)

    # Delete images from cloudinary
    deletePropertyImages(property["img_links"])
    deleteFloorPlanImages(property["floor_plans"])

    # Delete the document from firebase
    deletePropertyFromFirebase(id)

    return redirect("/properties")



if __name__ == '__main__':
    app.run(debug=True)

# CONTACT US

# Add additional data fields in app