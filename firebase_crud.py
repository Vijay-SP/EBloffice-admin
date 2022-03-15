import firebase_admin
from firebase_admin import credentials, firestore, storage
import datetime
import re

# Initialize Firestore DB
cred = credentials.Certificate('firebase-private-key.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Fetch the buyers list and return


def fetchBuyers():
    users_ref = db.collection("Users").where("isBroker", "==", False)
    usersStream = users_ref.stream()
    usersData = []
    for user in usersStream:
        usersData.append(user.to_dict())
    return usersData

# Fetch the brokers list and return


def fetchProperties():
    prop_ref = db.collection("Properties")
    propStream = prop_ref.stream()
    propData = []
    for prop in propStream:
        item = prop.to_dict()
        item["id"] = prop.id
        propData.append(item)
    return propData




def fetchProperty(id):
    prop_ref = db.collection("Properties").document(id).get()
    property = prop_ref.to_dict()
    property["id"] = prop_ref.id
    return property


def fetchUser(id):
    user_ref = db.collection("Users").document(id).get()
    user = user_ref.to_dict()
    user["id"] = user_ref.id
    return user


def checkNum(string):
    if string != '':
        try:
            return int(string)
        except:
            return None
    else:
        return None


def checkValue(string):
    if string != '':
        return string
    else:
        return None


def dataMap(request, img_url_list, floor_plan_img_list):
    # get the data fields

    # Name
    name = request.form.get("name")

    # Featured
    isFeatured = bool(request.form.get("isFeatured"))

    # Description
    description = request.form.get("description")

    # Details
    price = checkValue(request.form.get("price"))
    num_price = int(re.sub("[^0-9]", "", price))
    prop_size = checkValue(request.form.get("prop_size").strip())
    prop_type = checkValue(request.form.get("prop_type").strip())
    prop_status = checkValue(request.form.get("prop_status").strip())

    # Additional Details
    offices = checkNum(request.form.get("offices"))
    meeting_rooms = checkNum(request.form.get("meeting_rooms"))
    private_offices = checkNum(request.form.get("private_offices"))
    coworking_desks = checkNum(request.form.get("coworking_desks"))

    # Address Details
    address = checkValue(request.form.get("address").strip())
    city = checkValue(request.form.get("city").strip())
    country = checkValue(request.form.get("country").strip())
    zip = checkValue(request.form.get("zip"))

    # features
    features_str = checkValue(request.form.get("features"))
    features = list(map(lambda x: x.strip(), features_str.split(",")))
    if features[len(features)-1] == "":
        features.pop()
    if features[0] == "":
        features.pop(0)

    # Google Maps links
    map_url = checkValue(request.form.get("map_url"))

    data = {
        "additional_details": {
            "offices": offices,
            "coworking_desks": coworking_desks,
            "meeting_rooms": meeting_rooms,
            "private_offices": private_offices,
        },
        "price": num_price,
        "address": {
            "address": address,
            "city": city,
            "country": country,
            "zip": zip,
        },

        "desc": description,

        "details": {
            "price": price,
            "prop_size": prop_size,
            "prop_status": prop_status,
            "prop_type": [x.strip() for x in prop_type.split(",")]
,
        },
        "rating": {
            "1": {"0": 0},
            "2": {"0": 0},
            "3": {"0": 0},
            "4": {"0": 0},
            "5": {"0": 0},
        },
        "features": features,
        "floor_plans": floor_plan_img_list,
        "img_links": img_url_list,
        "map_url": map_url,
        "updated_on": datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"),
        "prop_name": name,
        "isFeatured": isFeatured,
    }
    return data


def uploadPropertyData(request, img_url_list, floor_plan_img_list):
    data = dataMap(request, img_url_list, floor_plan_img_list)
    # upload the data to firebase
    db.collection("Properties").add(data)


def updateEditedProperty(request, prop_id, img_url_list, floor_plan_img_list):
    data = dataMap(request, img_url_list, floor_plan_img_list)
    # upload the data to firebase
    db.collection("Properties").document(prop_id).update(data)


def deletePropertyFromFirebase(id):
    db.collection("Properties").document(id).delete()


def deleteContactFromFirebase(id):
    db.collection("ContactUs").document(id).delete()

def deleteAppointmenttFromFirebase(id):
    db.collection("Appointments").document(id).delete()




def updateDocs():
    prop_ref = db.collection("Properties")
    propStream = prop_ref.stream()
    for prop in propStream:
        prop_ref.document(prop.id).update(
        )


if __name__ == '__main__':
    updateDocs()
