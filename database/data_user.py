import pyrebase
from datetime import date
from firebase import firebase

Firebase = firebase.FirebaseApplication(
    "https://chatbot-73e7d-default-rtdb.firebaseio.com/", None
)

config = {
    "apiKey": "AIzaSyDZxQ86u3079cGCEL2dlKeOMQejT0jb2Ik",
    "authDomain": "chatbot-73e7d.firebaseapp.com",
    "projectId": "chatbot-73e7d",
    "databaseURL": "https://chatbot-73e7d-default-rtdb.firebaseio.com/",
    "storageBucket": "chatbot-73e7d.appspot.com",
    "messagingSenderId": "622784194359",
    "appId": "1:622784194359:web:a248b016adbb622769dcb2",
    "measurementId": "G-VSMY9CD1JW",
}
today = date.today()
firebase = pyrebase.initialize_app(config)
database = firebase.database()

user_name = "thai4362"


def get_user_data(user_name, today, Type, value):
    child = "User/" + user_name + "/" + f"{today}"
    data = Firebase.get(child, Type)
    return data.get(value)


def get_total_day(user_name, today):
    child = "User/" + user_name + "/" + f"{today}"
    data = Firebase.get(child, "Total")
    return data.get("Total day")


def updata_user(user_name, date, Type, cost):
    try:
        total_price = get_user_data(user_name, date, Type, "Total")

    except:
        total_price = 0
    try:
        list_cost = get_user_data(user_name, date, Type, "Cost")

    except:
        list_cost = []

    try:
        total_day = get_total_day(user_name, date)

    except:
        total_day = 0
    total_price = total_price + cost
    list_cost.append(cost)
    dataset = {"Cost": list_cost, "Total": total_price}

    total_day += cost
    dataset_day = {"Total day": total_day}
    database.child("User").child(user_name).child(date).child(Type).set(dataset)
    database.child("User").child(user_name).child(date).child("Total").set(dataset_day)
