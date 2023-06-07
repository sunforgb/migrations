import requests
import json
import datetime
def create_employee():
    body = {
        "user": {
            "email": "",
            "first_name": "",
            "last_name": "",
            "user_type": "employee",
            "password": ""
        },
        "contact": {
            "number": ""
        },
        "expirience": "",
        "salary": "",
        "rank": "Лейтенант",
        "information": ""
    }
    body["user"]["email"] = "fkirkorov@mvd.ru"
    body["user"]["first_name"] = "Филипп"
    body["user"]["last_name"] = "Киркоров"
    body["user"]["password"] = "fK1rB3$t"
    body["contact"]["number"] = "89278884321"
    body["expirience"] = "2"
    body["salary"] = "100000"
    body["information"] = "Люблю петь и стрелять в воздух"
    response_kir = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response_kir)
    body["user"]["email"] = "nbaskov@mvd.ru"
    body["user"]["first_name"] = "Николай"
    body["user"]["last_name"] = "Басков"
    body["user"]["password"] = "B@$k0vTr"
    body["contact"]["number"] = "89239457128"
    body["expirience"] = "3"
    body["salary"] = "120000.00"
    body["information"] = "Мое хобби - пить чай Золотая чаша"
    response_nik = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response_nik.json())
    body["user"]["email"] = "vmeladze@mvd.ru"
    body["user"]["first_name"] = "Валерий"
    body["user"]["last_name"] = "Меладзе"
    body["user"]["password"] = "M31@dz3B0$$"
    body["contact"]["number"] = "89853456139"
    body["expirience"] = "3"
    body["salary"] = "120000.00"
    body["information"] = "Мое хобби - смотреть телевизор"
    response_mel = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response_mel)
    body["user"]["email"] = "sbaretskii@mvd.ru"
    body["user"]["first_name"] = "Стас"
    body["user"]["last_name"] = "Баретский"
    body["user"]["password"] = "B@r1n_of_W0r1d"
    body["contact"]["number"] = "89676824583"
    body["expirience"] = "3"
    body["salary"] = "120000.00"
    body["information"] = "Мое хобби - пивные банки"
    response_stas = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response_stas)
    body["user"]["email"] = "mgalkin@mvd.ru"
    body["user"]["first_name"] = "Максим"
    body["user"]["last_name"] = "Галкин"
    body["user"]["password"] = "G@140n0k"
    body["contact"]["number"] = "89257592361"
    body["expirience"] = "4"
    body["salary"] = "140000.00"
    body["information"] = "Мое хобби - ухаживать за пенсионерами"
    response_max = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response_max)
    body["user"]["email"] = "ushatunov@mvd.ru"
    body["user"]["first_name"] = "Юрий"
    body["user"]["last_name"] = "Шатунов"
    body["user"]["password"] = " "
    body["contact"]["number"] = "89247568247"
    body["expirience"] = "4"
    body["salary"] = "140000.00"
    body["information"] = "Мое хобби - классика"
    response_yur = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response_yur)

def analyst_create():
    body = {
    "user": {
        "email": "dkuzmich@mvd.ru",
        "first_name": "Данила",
        "last_name": "Кузьмич",
        "user_type": "analyst",
        "password": "Q@_th3_B3$t!"
    },
    "contact": {
        "number": "89265451275"
    },
    "expirience": "5",
    "salary": "300000.00",
    "rank": "Капитан",
    "information": "Мое хобби - тестировать все подряд и писать отчеты"
    }
    response = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response)

def department_employee_set():
    body = {
        "user": {
            "department": [
                {
                    "id": "1"
                }
            ]
        }
    }
    res = requests.patch("http://185.231.153.231:8000/api/employees/2", json=body)
    print(res)
    res = requests.patch("http://185.231.153.231:8000/api/employees/3", json=body)
    body["user"]["department"] = [{"id": "2"}]
    res = requests.patch("http://185.231.153.231:8000/api/employees/4", json=body)
    print(res)
    res = requests.patch("http://185.231.153.231:8000/api/employees/5", json=body)
    print(res)
    body["user"]["department"] = [{"id": "3"}]
    res = requests.patch("http://185.231.153.231:8000/api/employees/6", json=body)
    print(res)
    res = requests.patch("http://185.231.153.231:8000/api/employees/7", json=body)
    print(res)
    body["user"]["department"] = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    res = requests.patch("http://185.231.153.231:8000/api/employees/8", json=body)
    print(res)


def create_migrants():
    body = {
        "contact": {
            "number": "87459235715"
        },
        "citizenship": {
            "code": "3",
            "name": "Турция"
        },
        "document": {
            "serial_number": "4585934723",
            "issued_by": "ГУ МВД по городу Москва",
            "issued_when": str(datetime.date.today()),
            "expires_when": str(datetime.date.today())
        },
        "name": "Олег Тиньков",
        "address": "Москва, Меньжинского 27, к 1",
        "birthday": str(datetime.date.today()),
        "birthday_place": "Турция",
        "profession": "Банкир"
    }
    res = requests.post("http://185.231.153.231:8000/api/migrants/", json=body)
    print(res.json())
    body["contact"]["number"] = "88259457634"
    body["citizenship"]["name"] = "Узбекистан"
    body["document"]["serial_number"] = "9541675234"
    body["document"]["issued_by"] = "ГУ МВД по городу Курск"
    body["name"] = "Сергей Жуков"
    body["address"] = "Москва, Кутузовский проспект 18, кв 17"
    body["profession"] = "Разнорабочий"
    res = requests.post("http://185.231.153.231:8000/api/migrants/", json=body)
    print(res.json())
    body["contact"]["number"] = "89276541934"
    body["citizenship"]["name"] = "Гондурас"
    body["document"]["serial_number"] = "1280583725"
    body["document"]["issued_by"] = "ГУ МВД по городу Москва"
    body["name"] = "Полина Гагарина"
    body["address"] = "Москва, Новый Арбат, д 32, кв 18"
    body["profession"] = "Певица"
    res = requests.post("http://185.231.153.231:8000/api/migrants/", json=body)
    print(res.json())


def create_dep_dir():
    body = {
        "user": {
            "email": "",
            "first_name": "",
            "last_name": "",
            "user_type": "department_dir",
            "password": ""
        },
        "contact": {
            "number": ""
        },
        "expirience": "",
        "salary": "",
        "rank": "Майор",
        "information": ""
    }
    body["user"]["email"] = "mvaretsa@mvd.ru"
    body["user"]["password"] = "$tr0ng_D@t@_Ru13"
    body["user"]["first_name"] = "Мария"
    body["user"]["last_name"] = "Вареца"
    body["contact"]["number"] = "86459234571"
    body["expirience"] = "5"
    body["salary"] = "250000.00"
    body["information"] = "Мне нравятся большие данные"
    response = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response.json())
    body["user"]["email"] = "dbarinov@mvd.ru"
    body["user"]["first_name"] = "Дмитрий"
    body["user"]["last_name"] = "Баринов"
    body["user"]["password"] = "B@r1n0_f"
    body["contact"]["number"] = "86548341258"
    body["expirience"] = "1"
    body["salary"] = "15000.00"
    body["information"] = "я Русский!"
    response = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response.json())
    body["user"]["email"] = "aermilov@mvd.ru"
    body["user"]["first_name"] = "Андрей"
    body["user"]["last_name"] = "Ермилов"
    body["user"]["password"] = "B@$$keT_!"
    body["contact"]["number"] = "89276541294"
    body["expirience"] = "10"
    body["salary"] = "500000.00"
    body["information"] = "Я лучший руководитель и баскетболист"
    response = requests.post("http://185.231.153.231:8000/api/employees/", json=body)
    print(response.json())


def main():
    #create_employee()
    #analyst_create()
    #department_employee_set()
    create_migrants()
    #create_dep_dir()


if __name__ == '__main__':
    main()