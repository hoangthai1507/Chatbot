# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from bs4 import BeautifulSoup
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database import getdata
import requests


class ActionFuelPrice(Action):

    def name(self) -> Text:
        return "action_fuel_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        price = getdata.getdata(0, "gas")
        dispatcher.utter_message(text=f"{price}")
   
        
class ActionGold(Action):

    def name(self) -> Text:
        return "action_jenewry_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        
        dispatcher.utter_message(text=f"vang 5 trieu")