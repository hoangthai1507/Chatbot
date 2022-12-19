from firebase import firebase
# from datetime import date
#
# yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)
# from datetime import date


# today = date.today()
Firebase = firebase.FirebaseApplication(
    "https://chatbot-b8f03-default-rtdb.firebaseio.com/", None
)

# name_data = input("name data: ")
# data_day = "Get_infor/" + f"{today}"
# print
# result = Firebase.get(data_day, "coffee")

# print(result)


# name_product = input("name_product:")
# day = input("day:")
# value = input("value: ")
# brand = input("brand: ")


def get_analyse(
    name_product, day, value
):  # truyen vao 3 gia tri la ten cua ten cua san pham can phan tich, ngay phan tich, gia tri can phan tich
    child = "ANALYSE" + "/" + day
    data = Firebase.get(child, name_product)
    return data.get(value)


# print(get_analyse(name_product, day, value))


def get_price(
    name_product, brand, day, value
):  # truyen vao 4 gia tri la ten cua ten cua san pham can phan tich, ngay phan tich, gia tri can phan tich, thuong hieu
    child = "PRICE" + "/" + day + "/" + name_product
    data = Firebase.get(child, brand)
    print(type(data))
    return data.get(value)


# print(get_price(name_product, brand, day, value))


def get_terms(name):  # truyen vao ten cua thuat ngu can phan tich
    return Firebase.get("TERMS", name).get("terms")


# print(get_terms(input("name: ")))


def get_list_term(name):
    terms_list = []
    terms = Firebase.get("TERMS", None)
    for i in terms:
        if terms.get(f"{i}").get("type") == name:
            terms_list.append(terms.get(f"{i}").get("terms"))

    return terms_list
