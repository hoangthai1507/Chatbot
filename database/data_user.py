import pyrebase
from datetime import date
from firebase import firebase
from datetime import datetime
import re

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



def StrToDate(Date):
    datetime_object = datetime.strptime(Date, "%Y-%m-%d")
    return datetime_object


def get_spending_day(user_name, today, Type, value):  ####################
    child = "User/" + user_name + "/" + f"{StrToDate(today).month}" "/" + f"{today}"
    #child = "User/" + user_name + "/" + f"{today.month}" "/" + f"{today}"

    data = Firebase.get(child, Type)

    return data.get(value)


def get_spending_month(user_name, month, value):
    child = "User/" + user_name + "/" + f"{month}"
    data = Firebase.get(child, "Summary")

    return data.get(value)


def get_total_month(user_name, date):
    child = "User/" + user_name + "/" + f"{StrToDate(date).month}" + "/" + "Summary"
    #child = "User/" + user_name + "/" + f"{date.month}" + "/" + "Summary"

    data = Firebase.get(child, "Total spending")
    if data == None:
        data = 0
    return data


def get_total_day(user_name, today):
    child = "User/" + user_name + "/" + f"{StrToDate(today).month}"
    # child = "User/" + user_name + "/" + f"{today.month}"

    data = Firebase.get(child, f"{today}")
    return data.get("Total")


def get_salary(user_name, month):
    child = "User/" + user_name + "/" + f"{month}"
    data = Firebase.get(child, "Summary")
    return data.get("Salary")


def updata_user(user_name, month, date, Type, cost):
    try:
        total_price = get_spending_day(user_name, date, Type, "Total")

    except:
        total_price = 0
    try:
        value_month = get_spending_month(user_name, month, Type)
        if value_month == None:
            value_month = 0
    except:
        value_month = 0
    try:
        list_cost = get_spending_day(user_name, date, Type, "Cost")

    except:
        list_cost = []

    try:
        total_day = get_total_day(user_name, date)

    except:
        total_day = 0
    try:
        total_month = get_total_month(user_name, date)
    except:
        total_month = 0
    value_month += cost
    total_month += cost
    total_price += cost
    list_cost.append(cost)
    dataset = {"Cost": list_cost, "Total": total_price}
    total_day += cost

    database.child("User").child(user_name).child(month).child(date).child(Type).set(
        dataset
    )
    database.child("User").child(user_name).child(month).child(date).child("Total").set(
        total_day
    )
    database.child("User").child(user_name).child(month).child("Summary").child(
        "Total spending"
    ).set(total_month)
    database.child("User").child(user_name).child(month).child("Summary").child(
        Type
    ).set(value_month)


def updata_salary_user(user_name, date, salary):
    database.child("User").child(user_name).child(StrToDate(date).month).child(
        "Summary"
    ).child("Salary").set(salary)


def change_money(k_money, m_money):
    if k_money != None and m_money != None:
        k_money = int([float(x) for x in re.findall(r"-?\d+\.?\d*", k_money)][0]) * 1000
        m_money = (
            int([float(x) for x in re.findall(r"-?\d+\.?\d*", m_money)][0]) * 1000000
        )
        money = k_money + m_money
        return money
    else:
        if k_money != None:
            return (
                int([float(x) for x in re.findall(r"-?\d+\.?\d*", k_money)][0]) * 1000
            )
        else:
            return (
                int([float(x) for x in re.findall(r"-?\d+\.?\d*", m_money)][0])
                * 1000000
            )


def check_spending(user_name, month, today):
    text = ""
    try:
        Salary = get_salary(user_name, month)
        if Salary == None:
            text = "B???n ch??a c???p nh???t l????ng th??ng n??y! Vui l??ng c???p nh???t l????ng ????? h??? tr??? vi???c ??o l?????ng"
            return text
    except:
        Salary = -1
        text = "B???n ch??a c???p nh???t l????ng th??ng n??y! Vui l??ng c???p nh???t l????ng ????? h??? tr??? vi???c ??o l?????ng"
        return text
    try:
        Total_spending = get_total_day(user_name, today)
        if Total_spending == None:
            Total_spending = 0
    except:
        Total_spending = 0

    if Salary == Total_spending:
        text = "B???n ???? s??? d???ng h???t l????ng th??ng n??y!! Vui l??ng h???n ch??? s??? d???ng ti???n l???i ho???c c??? g???ng t??m th??m thu nh???p cho th??ng n??y!! :>"
        return text
    elif Salary < Total_spending:
        text = "B???n ???? s??? d???ng l??? ti???n l????ng th??ng n??y!! Vui l??ng h???n ch??? s??? d???ng ti???n l???i ho???c c??? g???ng t??m th??m thu nh???p cho th??ng n??y!! :>"
        return text
    
def statistical_day(user_name, today):
    food = None
    personal = None
    recreation = None
    housing = None
    try:
        food = get_spending_day(user_name, today, "food_section", "Total")
    except:
        food = 0
    try:
        personal = get_spending_day(user_name, today, "personal" or "personal_section", "Total")
    except:
        personal = 0
    try:
        recreation = get_spending_day(user_name, today, "recreation_section", "Total")
    except:
        recreation = 0
    try:
        housing = get_spending_day(user_name, today, "housing_section", "Total")
    except:
        housing = 0
    return [food, personal, recreation, housing]


def statistical_month(user_name, month):
    List_data = []
    food = None
    personal = None
    recreation = None
    housing = None
    try:
        food = get_spending_month(user_name, month, "food_section")
    except:
        food = 0
    try:
        personal = get_spending_month(user_name, month, "personal_section")
    except:
        personal = 0
    try:
        recreation = get_spending_month(user_name, month, "recreation_section")
    except:
        recreation = 0
    try:
        housing = get_spending_month(user_name, month, "housing_section")
    except:
        housing = 0
    return [food, personal, recreation, housing]

