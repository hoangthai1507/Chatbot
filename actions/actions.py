# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from database import getdata
from database import getdate

from database import data_user

user_name = "thai4362"


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
        print(day_entity)
        status = next(tracker.get_latest_entity_values("status"), None)
        if day_entity == "hôm nay":
            day = getdate.get_today()
        elif day_entity == "hôm qua":
            day = getdate.get_yesterday()
        else:
            day = day_entity

        try:
            Price = getdata.get_price("price", name_product, day, "Price")
            print(Price)
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
                "ngày " + f"{day}, {name_product} có các loại giá sau: \n"
                + "giá mua là "
                + f"{Price} vnd."
                + "\n"
                + "giá bán là "
                + f"{Purchase_price} vnd."
                + "\n"
                + "giá chuyển nhượng là "
                + f"{Transfer_price} vnd."
            )
        elif status == "mua" or status == "giá mua":
            text = (
                "giá mua " + name_product + " hôm " + f"{day}"
                " là: " + f"{Price} vnd." + "\n"
            )
        elif status == "bán" or status == "giá bán":
            text = (
                "giá bán " + name_product + " hôm " + f"{day}"
                " là: " + f"{Purchase_price} vnd." + "\n"
            )
        elif status == "giá chuyển nhượng":
            text = (
                "giá chuyển nhượng " + name_product + " hôm " + f"{day}"
                " là: " + f"{Transfer_price} vnd." + "\n"
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
        print(name_product)
        day_entity = next(tracker.get_latest_entity_values("day"), None)
        status = next(tracker.get_latest_entity_values("status"), None)
        print(status)
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

        if status and day_entity and name_product:
            if "mua" in status:
                price = price_buy_today if day == getdate.get_today() else price_buy_yesterday
                text = (
                        f"giá mua vàng " + name_product + " hôm " + f"{day} là "
                        + f"{price},000 vnd."
                        + "\n"
                )
            else :
                price = price_sell_today if day == getdate.get_today() else price_sell_yesterday
                text = (
                        f"giá bán vàng " + name_product + " hôm " + f"{day} là "
                        + f"{price},000 vnd."
                        + "\n"
                )
        elif status and name_product:
            price = price_buy_today if "mua" in status else price_sell_today
            t = "mua" if "mua" in status else "bán"
            text = (
                    f"giá {t} vàng " + name_product + " hôm " + f"{day} là "
                    + f"{price},000 vnd."
                    + "\n"
            )
        elif name_product:
            price_b = price_buy_today
            price_s = price_sell_today
            if day == getdate.get_today():
                text = (
                        f"giá mua vàng " + name_product + " hôm nay " + f"({day}) là "
                        + f"{price_b},000 vnd."
                        + "\n"
                        + f"giá bán vàng " + name_product + " hôm nay " + f"({day}) là "
                        + f"{price_s},000 vnd."
                        + "\n"
                )
            else :
                price_b = price_buy_yesterday
                price_s = price_sell_yesterday
                text = (
                        f"giá mua vàng " + name_product + " hôm qua " + f"({day}) là "
                        + f"{price_b},000 vnd."
                        + "\n"
                        + f"giá bán vàng " + name_product + " hôm qua " + f"({day}) là "
                        + f"{price_s},000 vnd."
                        + "\n"
                )
        dispatcher.utter_message(text)


class ActionAnaly(Action):
    def name(self) -> Text:
        return "action_summarize_explain"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        gold = None
        coffee = None
        meat = None
        stock = None
        date = next(tracker.get_latest_entity_values("day"), None)
        try:
            gold = next(tracker.get_latest_entity_values("name_jenewry_summarize"), None)
        except:
            print("Not gold!")
        try:
            coffee = next(tracker.get_latest_entity_values("name_coffee"), None)
        except:
            print("Not coffee!")
        try:
            meat = next(tracker.get_latest_entity_values("name_meat"), None)
        except:
            print("Not meat!")
        try:
            meat = next(tracker.get_latest_entity_values("food_section"), None)
        except:
            print("Not meat!")
        try:
            stock = next(tracker.get_latest_entity_values("name_stock"), None)
        except:
            print("Not stock!")

        if date == "hôm nay" or date == None:
            day = getdate.get_today()
        elif date == "hôm qua":
            day = getdate.get_yesterday()
        else:
            day = date
        if gold != None:
            try:
                detail = getdata.get_analyse("gold", day, "price_gold_detail")
            except:
                print("can not find detail of gold!")
                return
            try:
                summary = getdata.get_analyse("gold", day, "price_gold_summary")
            except:
                print("can not find summary of gold")
                return
            text = (
                "phân tích vàng hôm " + f"{day}"
                " là:\n"
                + "Chi tiết : "
                + f"{detail}"
                + "\n\n"
                + "Tóm lược : "
                + f"{summary}"
            )

        elif coffee != None:
            try:
                detail = getdata.get_analyse("coffee", day, "price_coffee_detail")
            except:
                print("can not find detail of coffee!")
                return
            try:
                summary = getdata.get_analyse("coffee", day, "price_cofffee_summary")
            except:
                print("can not find summary of coffee")
                return
            text = (
                "phân tích cà phê hôm " + f"{day}"
                " là:\n"
                + "Chi tiết : "
                + f"{detail}"
                + "\n\n"
                + "Tóm lược : "
                + f"{summary}"
            )
        elif meat != None:
            try:
                detail = getdata.get_analyse("meat", day, "price_meat_detail")
            except:
                print("can not find detail of meat!")
                return
            try:
                summary = getdata.get_analyse("meat", day, "price_meat_summary")
            except:
                print("can not find summary of meat")
                return
            text = (
                "phân tích giá thịt hôm " + f"{day}"
                " là:\n"
                + "Chi tiết : "
                + f"{detail}"
                + "\n\n"
                + "Tóm lược : "
                + f"{summary}"
            )

        elif stock != None:
            daily = None
            weekly = None
            try:
                daily = getdata.get_analyse("stock", day, "Stock_daily_analy")
            except:
                print("can not find daily analyse of stock!")
                return
            try:
                weekly = getdata.get_analyse("stock", day, "stock_weekly_analy")
            except:
                print("can not find weekly analyse of stock!")

            if weekly != None:
                text = (
                    "phân tích chứng khoán hôm " + f"{day}"
                    " là:\n"
                    + "phân tích chứng khoán theo ngày: "
                    + f"{daily}"
                    + "\n"
                    + "phân tích chứng khoán theo tuần: "
                    + f"{weekly}"
                )
            else:
                text = (
                    "phân tích chứng khoán hôm " + f"{day}"
                    " là:\n" + "phân tích chứng khoán theo ngày: " + f"{daily}" + "\n"
                )
        else:
            text = "có thể bạn đang muốn biết về phân tích một loại hàng hoá nào đó, vui lòng nhập cụ thể hơn!"

        dispatcher.utter_message(text)
        return


class ActionSubsistence(Action):
    def name(self) -> Text:
        return "action_Subsistence"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        k_money = None
        m_money = None
        money = 0
        food = None
        hous = None
        recreation = None
        personal = None
        day_entity = next(tracker.get_latest_entity_values("day"), None)
        if day_entity == "hôm nay" or day_entity == None:
            date = getdate.get_today()
        elif day_entity == "hôm qua":
            date = getdate.get_yesterday()
        else:
            date = day_entity
        print(date)
        print(type(date))
        try:
            k_money = next(tracker.get_latest_entity_values("k_money"), None)
        except:
            print("no k money")
        try:
            m_money = next(tracker.get_latest_entity_values("m_money"), None)
        except:
            print("no m money")
        try:
            food = next(tracker.get_latest_entity_values("food_section"), None)
        except:
            print("problem with food!")
        try:
            hous = next(tracker.get_latest_entity_values("housing_section"), None)
        except:
            print("problem with house!")
        try:
            recreation = next(
                tracker.get_latest_entity_values("recreation_section"), None
            )
        except:
            print("problem with recreation!")
        try:
            personal = next(tracker.get_latest_entity_values("personal_section"), None)
        except:
            print("problem with recreation!")
        try:
            money = data_user.change_money(k_money, m_money)
        except:
            print("problem with money!")
            return
        if food != None:

            data_user.updata_user(
                user_name, data_user.StrToDate(date).month, date, "food_section", money
            )
            text = (
                "Đã thêm "
                + "{0:,}".format(money)
                + " vào danh sách chi tiêu cho thực phẩm"
            )
        elif hous != None:

            data_user.updata_user(
                user_name,
                data_user.StrToDate(date).month,
                date,
                "housing_section",
                money,
            )
            text = (
                "Đã thêm "
                + "{0:,}".format(money)
                + " vào danh sách chi tiêu cho sinh hoạt"
            )
        elif recreation != None:

            data_user.updata_user(
                user_name,
                data_user.StrToDate(date).month,
                date,
                "recreation_section",
                money,
            )
            text = (
                "Đã thêm "
                + "{0:,}".format(money)
                + " vào danh sách chi tiêu cho giải trí"
            )
        elif personal != None:
            data_user.updata_user(
                user_name, data_user.StrToDate(date).month, date, "personal", money
            )
            text = (
                "bạn đã dùng "
                + "{0:,}".format(money)
                + " vào danh sách chi tiêu cho mua sắm"
            )
        else:
            text = "có vẻ như bạn muốn nhập liệu thông tin tiêu dùng, vui lòng nhập một cách cự thể hơn!"

        dispatcher.utter_message(text)
        check = data_user.check_spending(
            user_name, data_user.StrToDate(date).month, date
        )
        if check != "":
            dispatcher.utter_message(check)
        return


class ActionSalary(Action):
    def name(self) -> Text:
        return "action_Salary_money"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        k_money = None
        m_money = None
        month_entity = next(tracker.get_latest_entity_values("month"), None)
        if month_entity == "tháng này" or month_entity == None:
            date = getdate.get_today()
        elif month_entity == "tháng trước" or month_entity == "tháng qua":
            date = getdate.last_month()
        else:
            date = month_entity
        try:
            k_money = next(tracker.get_latest_entity_values("k_money"), None)
        except:
            print("no k money")
        try:
            m_money = next(tracker.get_latest_entity_values("m_money"), None)
        except:
            print("no m money")
        try:
            money = data_user.change_money(k_money, m_money)
        except:
            print("problem with money!")
            return
        if money != None:
            data_user.updata_salary_user(user_name, date, money)
            text = (
                "Đẫ cập nhật lương tháng "
                + f"{data_user.StrToDate(date).month}"
                + " là "
                + "{0:,}".format(money)
                + "vnd"
            )
        else:
            text = "Có sự cố trong quá trình cập nhật lương, vui lòng nhập lại!"

        dispatcher.utter_message(text)
        return


class ActionTotal(Action):
    def name(self) -> Text:
        return "action_Total_money"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        money = None
        food = None
        housing = None
        recreation = None
        personal = None
        day_entity = next(tracker.get_latest_entity_values("day"), None)
        if day_entity == "hôm nay" or day_entity == None:
            date = getdate.get_today()
        elif day_entity == "hôm qua":
            date = getdate.get_yesterday()
        else:
            date = day_entity

        try:
            food = next(tracker.get_latest_entity_values("food"), None)
        except:
            print("problem with food!")
        try:
            personal = next(tracker.get_latest_entity_values("personal"), None)
        except:
            print("problem with personal!")
        try:
            recreation = next(tracker.get_latest_entity_values("recreation"), None)
        except:
            print("problem with recreation!")
        try:
            housing = next(tracker.get_latest_entity_values("housing"), None)
        except:
            print("problem with housing!")

        if food != None:
            try:
                total_food = data_user.get_spending_day(
                    user_name, date, "food_section", "Total"
                )
                text = (
                    "Ngày "
                    + f"{data_user.StrToDate(date).date}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_food)
                    + "vnd "
                    + "cho việc "
                    + f"{food}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong ngày hôm nay!"
                )
                return
        elif housing != None:
            try:
                total_housing = data_user.get_spending_day(
                    user_name, date, "housing_section", "Total"
                )
                text = (
                    "Ngày "
                    + f"{data_user.StrToDate(date).date}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_housing)
                    + "vnd "
                    + "cho việc "
                    + f"{housing}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong ngày hôm nay!"
                )
                return
        elif recreation != None:
            try:
                total_recreation = data_user.get_spending_day(
                    user_name, date, "recreation_section", "Total"
                )
                text = (
                    "Ngày "
                    + f"{data_user.StrToDate(date).date}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_recreation)
                    + "vnd "
                    + "cho việc "
                    + f"{recreation}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong ngày hôm nay!"
                )
                return
        elif personal != None:
            try:
                total_personal = data_user.get_spending_day(
                    user_name, date, "personaln_section", "Total"
                )
                text = (
                    "Ngày "
                    + f"{data_user.StrToDate(date).date}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_personal)
                    + "vnd "
                    + "cho việc "
                    + f"{personal}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong ngày hôm nay!"
                )
                return
        else:
            try:
                total = data_user.get_total_day(user_name, date)
                text = (
                    "Ngày "
                    + f"{data_user.StrToDate(date).date}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total)
                    + "vnd ngày hôm nay"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong ngày hôm nay!"
                )
                return
        dispatcher.utter_message(text)
        return


class ActionTotalMonth(Action):
    def name(self) -> Text:
        return "action_Total_money_month"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        food = None
        housing = None
        recreation = None
        personal = None
        month_entity = next(tracker.get_latest_entity_values("month"), None)
        if month_entity == "tháng này" or month_entity == None:
            month = getdate.get_today()
        elif month_entity == "tháng trước" or month_entity == "tháng qua":
            month = getdate.last_month()
        else:
            month = month_entity

        try:
            food = next(tracker.get_latest_entity_values("food"), None)
        except:
            print("problem with food!")
        try:
            personal = next(tracker.get_latest_entity_values("personal"), None)
        except:
            print("problem with personal!")
        try:
            recreation = next(tracker.get_latest_entity_values("recreation"), None)
        except:
            print("problem with recreation!")
        try:
            housing = next(tracker.get_latest_entity_values("housing"), None)
        except:
            print("problem with housing!")

        if food != None:
            try:
                total_food = data_user.get_spending_month(
                    user_name, data_user.StrToDate(month).month, "food_section"
                )
                text = (
                    "Tháng "
                    + f"{data_user.StrToDate(month).month}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_food)
                    + "vnd "
                    + "cho việc "
                    + f"{food}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong tháng này!"
                )
                return
        elif housing != None:
            try:
                total_housing = data_user.get_spending_month(
                    user_name, data_user.StrToDate(month).month, "housing_section"
                )
                text = (
                    "Tháng "
                    + f"{data_user.StrToDate(month).month}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_housing)
                    + "vnd "
                    + "cho việc "
                    + f"{housing}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong tháng này!"
                )
                return
        elif recreation != None:
            try:
                total_recreation = data_user.get_spending_month(
                    user_name, data_user.StrToDate(month).month, "recreation_section"
                )
                text = (
                    "Tháng "
                    + f"{data_user.StrToDate(month).month}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_recreation)
                    + "vnd "
                    + "cho việc "
                    + f"{recreation}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong tháng này!"
                )
                return
        elif personal != None:
            try:
                total_personal = data_user.get_spending_month(
                    user_name, data_user.StrToDate(month).month, "personal_section"
                )
                text = (
                    "Tháng "
                    + f"{data_user.StrToDate(month).month}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total_personal)
                    + "vnd "
                    + "cho việc "
                    + f"{personal}"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong tháng này!"
                )
                return
        else:
            try:
                total = data_user.get_total_month(user_name, month)
                text = (
                    "Tháng "
                    + f"{data_user.StrToDate(month).month}"
                    + " bạn đã sử dụng tổng cộng "
                    + "{0:,}".format(total)
                    + "vnd"
                )
            except:
                dispatcher.utter_message(
                    "Có lỗi trong quá trình trích xuất thông tin, hoặc là bạn chưa nhập thông tin này trong tháng này!"
                )
                return
        dispatcher.utter_message(text)
        return

class ActionStatistic(Action):
    def name(self) -> Text:
        return "action_Statistical"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        mon = getdate.last_month()
        mon = data_user.StrToDate(mon).month

        if next(tracker.get_latest_entity_values("food"), None):
            data = {"title": f"Phân bổ chi tiêu cho việc ăn uống tháng {mon}/2022",
                    "labels": ["ăn uống", "mua sắm", "giải trí", "sinh hoạt"],
                    "backgroundColor": ["#36a2eb", "#ffcd56", "#ff6384", "#009688", "#c45850"],
                    "chartsData": data_user.statistical_month(user_name, mon), "chartType": "scatter",
                    "displayLegend": "true"}

            message = {"payload": "chart", "data": data}

            dispatcher.utter_message(text="Đây là bảng phân bố chi tiêu của bạn", json_message=message)

        else :
            data = {"title": f"Phân bổ chi tiêu tháng {mon}/2022", "labels": ["ăn uống", "mua sắm", "giải trí", "sinh hoạt"],
                    "backgroundColor": ["#36a2eb", "#ffcd56", "#ff6384", "#009688", "#c45850"],
                    "chartsData": data_user.statistical_month(user_name, mon), "chartType": "doughnut", "displayLegend": "true"}

            message = {"payload": "chart", "data": data}

        dispatcher.utter_message(text="Đây là bảng phân bố chi tiêu của bạn", json_message=message)

