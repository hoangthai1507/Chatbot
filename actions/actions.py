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

        elif "xăng" in tracker.latest_message["text"]:
            price = getdata.get_price("gas", "Xăng RON 95-III", date, "price")
            msg = f"giá Xăng RON 95-III {day} ({date}) là {price} vnd còn "
            price = getdata.get_price("gas", "Xăng E5 RON 92-II", date, "price")
            msg += f"giá Xăng E5 RON 92-II {day} ({date}) là {price} vnd"
            dispatcher.utter_message(text=f"{msg}")

        elif "dầu" in tracker.latest_message["text"]:
            price = getdata.get_price("gas", "Dầu hỏa", date, "price")
            msg = f"giá Dầu hỏa {day} ({date}) là {price} vnd còn "
            price = getdata.get_price("gas", "Dầu diesel", date, "price")
            msg += f"giá Dầu diesel {day} ({date}) là {price} vnd "
            dispatcher.utter_message(text=f"{msg}")
        else:
            dispatcher.utter_message(
                text=f"có vẻ bạn đang hỏi về xăng, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            )


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
            dispatcher.utter_message(
                text=f"có vẻ bạn đang hỏi về cà phê, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            )


class ActionTerm(Action):
    def name(self) -> Text:
        return "action_term_explain"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        term = next(tracker.get_latest_entity_values("terms"), None)
        explain = ""

        try:
            explain = getdata.get_terms(term)
        except:
            print(term)

        if explain:
            msg = f"{explain}"
            dispatcher.utter_message(text=msg)

        else:
            dispatcher.utter_message(
                text=f"có vẻ bạn đang hỏi về thuật ngữ đầu tư chứng khoán, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ!"
            )


class ActionMoney(Action):
    def name(self) -> Text:
        return "action_money_price"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name_product = next(tracker.get_latest_entity_values("name_money"), None)
        day_entity = next(tracker.get_latest_entity_values("day"), None)
        status = next(tracker.get_latest_entity_values("status"), None)
        if day_entity == "hôm nay":
            day = getdate.get_today()
        elif day_entity == "hôm qua":
            day = getdate.get_yesterday()
        else:
            day = day_entity

        try:
            Price = getdata.get_price("price", name_product, day, "Price")
        except:
            dispatcher.utter_message(
                text=f"có vẻ bạn đang hỏi về tiền ngoại tệ, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            )
            return
        try:
            Purchase_price = getdata.get_price(
                "price", name_product, day, "Purchase price"
            )
        except:
            dispatcher.utter_message(
                text=f"có vẻ bạn đang hỏi về tiền ngoại tệ, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            )
            return
        try:
            Transfer_price = getdata.get_price(
                "price", name_product, day, "Transfer price"
            )
        except:
            dispatcher.utter_message(
                text=f"có vẻ bạn đang hỏi về tiền ngoại tệ, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            )
            return

        if status == None:
            text = (
                "giá " + name_product + " hôm " + f"{day}"
                " là:\n"
                + "giá mua: "
                + f"{Price}"
                + "\n"
                + "giá bán: "
                + f"{Purchase_price}"
                + "\n"
                + "giá chuyển nhượng: "
                + f"{Transfer_price}"
            )
        elif status == "mua" or status == "giá mua":
            text = (
                "giá " + name_product + " hôm " + f"{day}"
                " là: " + "giá mua: " + f"{Price}" + "\n"
            )
        elif status == "bán" or status == "giá bán":
            text = (
                "giá " + name_product + " hôm " + f"{day}"
                " là: " + "giá bán: " + f"{Purchase_price}" + "\n"
            )
        elif status == "giá chuyển nhượng":
            text = (
                "giá " + name_product + " hôm " + f"{day}"
                " là: " + "giá chuyển nhượng: " + f"{Transfer_price}" + "\n"
            )

        dispatcher.utter_message(text)


class ActionGold(Action):
    def name(self) -> Text:
        return "action_jenewry_price"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name_product = next(tracker.get_latest_entity_values("name_jenewry"), None)
        day_entity = next(tracker.get_latest_entity_values("day"), None)
        status = next(tracker.get_latest_entity_values("status"), None)
        if day_entity == "hôm nay" or day_entity == None:
            day = getdate.get_today()
        elif day_entity == "hôm qua":
            day = getdate.get_yesterday()
        else:
            day = day_entity
        try:
            price_buy_today = getdata.get_price(
                "gold", name_product, day, "price buy today"
            )
        except:
            text = f"có vẻ bạn đang hỏi về giá vàng, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            dispatcher.utter_message(text)
            return
        try:
            price_buy_yesterday = getdata.get_price(
                "gold", name_product, day, "price buy yesterday"
            )

        except:
            text = f"có vẻ bạn đang hỏi về giá vàng, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            dispatcher.utter_message(text)
            return
        try:
            price_sell_today = getdata.get_price(
                "gold", name_product, day, "price sell today"
            )
        except:
            text = f"có vẻ bạn đang hỏi về giá vàng, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            dispatcher.utter_message(text)
            return
        try:
            price_sell_yesterday = getdata.get_price(
                "gold", name_product, day, "price sell yesterday"
            )
        except:
            text = f"có vẻ bạn đang hỏi về giá vàng, bạn hãy thử đặt lại câu hỏi ngắn gọn hơn ạ !"
            dispatcher.utter_message(text)
            return
        if status == None:
            text = (
                "giá vàng " + name_product + " hôm " + f"{day}"
                " là:\n"
                + "giá mua hôm nay: "
                + f"{price_buy_today}"
                + "\n"
                + "giá bán hôm nay: "
                + f"{price_buy_yesterday}"
                + "\n"
                + "giá mua hôm qua: "
                + f"{price_sell_today}"
                + "\n"
                + "giá bán hôm qua: "
                + f"{price_sell_yesterday}"
                + "\n"
            )
        elif status == "mua" or status == "giá mua":
            text = (
                "giá vàng " + name_product + " hôm " + f"{day}"
                " là:\n"
                + "giá mua hôm nay: "
                + f"{price_buy_today}"
                + "\n"
                + "giá mua hôm qua: "
                + f"{price_sell_today}"
                + "\n"
            )
        elif status == "bán" or status == "giá bán":
            text = (
                "giá vàng " + name_product + " hôm " + f"{day}"
                " là:\n"
                + "giá bán hôm nay: "
                + f"{price_buy_yesterday}"
                + "\n"
                + "giá bán hôm qua: "
                + f"{price_sell_yesterday}"
                + "\n"
            )
        elif status == "mua" and day_entity == "hôm nay":
            text = (
                "giá vàng " + name_product + " hôm " + f"{day}"
                " là:\n" + "giá mua hôm nay: " + f"{price_buy_today}" + "\n"
            )
        elif status == "bán" and day_entity == "hôm nay":
            text = (
                "giá vàng " + name_product + " hôm " + f"{day}"
                " là:\n" + "giá bán hôm nay: " + f"{price_buy_yesterday}" + "\n"
            )

        dispatcher.utter_message(text)
