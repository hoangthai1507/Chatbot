# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import getdata
from database import getdate


class ActionFuelPrice(Action):
    def name(self) -> Text:
        return "action_fuel_price"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name_fuel = next(tracker.get_latest_entity_values("name_fuel"), None)
        day = next(tracker.get_latest_entity_values("day"), None)
        price = ""
        if day == "hôm qua":
            date = getdate.get_yesterday()
        else:
            date = getdate.get_today()
            day = "hôm nay"

        try:
            price = getdata.get_price("gas", name_fuel, date, "price")
        except:
            print(name_fuel)

        if price:
            msg = f"giá {name_fuel} {day} ({date}) là {price} vnd"
            dispatcher.utter_message(text=msg)

        elif "xăng" in tracker.latest_message['text']:
            price = getdata.get_price("gas", "Xăng RON 95-III", date, "price")
            msg = f"giá Xăng RON 95-III {day} ({date}) là {price} vnd còn "
            price = getdata.get_price("gas", "Xăng E5 RON 92-II", date, "price")
            msg += f"giá Xăng E5 RON 92-II {day} ({date}) là {price} vnd"
            dispatcher.utter_message(text=f"{msg}")

        elif "dầu" in tracker.latest_message['text']:
            price = getdata.get_price("gas", "Dầu hỏa", date, "price")
            msg = f"giá Dầu hỏa {day} ({date}) là {price} vnd còn "
            price = getdata.get_price("gas", "Dầu diesel", date, "price")
            msg += f"giá Dầu diesel {day} ({date}) là {price} vnd "
            dispatcher.utter_message(text=f"{msg}")
        else:
            dispatcher.utter_message(text=f"có vẻ bạn đang hỏi về xăng, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !")


class ActionCoffeePrice(Action):
    def name(self) -> Text:
        return "action_coffee_price"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name_coffee = next(tracker.get_latest_entity_values("name_coffee"), None)
        day = next(tracker.get_latest_entity_values("day"), None)
        price = ""
        if day == "hôm qua":
            date = getdate.get_yesterday()
        else:
            date = getdate.get_today()
            day = "hôm nay"

        try:
            price = getdata.get_price("coffee", name_coffee, date, "average price")
        except:
            print(name_coffee)

        if price:
            msg = f"giá cà phê {name_coffee} {day} ({date}) là {price} vnd 1kg"
            dispatcher.utter_message(text=msg)

        else:
            dispatcher.utter_message(text=f"có vẻ bạn đang hỏi về cà phê, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !")


class ActionGold(Action):
    def name(self) -> Text:
        return "action_jenewry_price"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"vang 5 trieu")
