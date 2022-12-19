from firebase import firebase
from datetime import date


today = date.today()
Firebase = firebase.FirebaseApplication(
    "https://chatbot-b8f03-default-rtdb.firebaseio.com/", None
)


data_day = "Get_infor/" + f"{today}"
print
result = Firebase.get(data_day, "coffee")

print(result)