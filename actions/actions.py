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


class ActionFuelPrice(Action):
    def name(self) -> Text:
        return "action_fuel_price"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        entity = next(tracker.get_latest_entity_values("name_fuel"), None)
        entity_list = ["Xăng RON 95-III", "Xăng E5 RON 92-II", "Dầu diesel", "Dầu hỏa"]
        # price = getdata.getdata(0, "gas")
        # t = "price"
        # if entity in entity_list:
        #     msg = f"giá {entity} hôm nay là {price[entity].get(t)} vnd"
        #     dispatcher.utter_message(text=msg)
        # elif "xăng" in entity:
        #     msg = f"giá {entity_list[0]} hôm nay là {price[entity_list[0]].get(t)} vnd còn {entity_list[1]} hôm nay là {price[entity_list[1]].get(t)} vnd"
        #     dispatcher.utter_message(text=msg)
        # elif "dầu" in entity:
        #     msg = f"giá {entity_list[2]} hôm nay là {price[entity_list[2]].get(t)} vnd còn {entity_list[3]} hôm nay là {price[entity_list[3]].get(t)} vnd"
        #     dispatcher.utter_message(text=msg)
        # else:
        #     dispatcher.utter_message(text=f"{price}")
        dispatcher.utter_message(text=f"xang 5 trieu")


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
