from django.shortcuts import render
from .models import Relevance, Geography, Skills
import requests


import json
import xml.etree.ElementTree as ET
import datetime


def index(request):
    return render(request, 'main/index.html')

def relevance(request):
    rel = Relevance.objects.all()
    return render(request, 'main/relevance.html', {'relevance':rel})

def geography(request):
    geo = Geography.objects.all()
    return render(request, 'main/geography.html', {'geography':geo})

def skills(request):
    skill = Skills.objects.all()
    return render(request, 'main/skills.html', {'skills':skill})

def recentVacancies(request):
    params = {
        'text':'"NAME:1c разработчик" OR "NAME:1c разработчик" OR "NAME:1с" OR "NAME:1c" OR "NAME:1 c" OR "NAME:1 с"',
        'per_page':10,
        'period':1,
        'order_by':'publication_time'
    }
    strHH = getJSON("https://api.hh.ru/vacancies", params)
    date = datetime.datetime.now().strftime('%d/%m/%Y')
    strCBRF = getJSON(f"https://cbr.ru/scripts/XML_daily.asp?date_req={date}", "")
    listHH = jsonToList(strHH)
    listCBRF = parseCBRF(strCBRF)
    convertListHH = convertCurrency(listHH, listCBRF)

    return render(request, 'main/recent.html', {'convertListHH':convertListHH})

def getJSON(url, params):
    resp = requests.get(url, params)
    return resp.text

def jsonToList(jsonHH):
    str = json.loads(jsonHH)
    result_list = []

    for item in str.get("items", []):
        name = "Не указано"
        responsibility = "Не указано"
        requirement = "Не указано"
        employer_name = "Не указано"
        salary_from = "Не указано"
        salary_currency = ""
        area_name = "Не указано"
        created_at = "Не указано"

        if item.get("name") is not None:
            name = item.get("name", "")
        if item.get("snippet") is not None:
            responsibility = item.get("snippet", {}).get("responsibility", "")
        if item.get("snippet") is not None:
            requirement = item.get("snippet", {}).get("requirement", "")
        if item.get("employer") is not None:
            employer_name = item.get("employer", {}).get("name", "")
        if item.get("salary") is not None and item.get("salary").get("from") is not None:
            salary_from = item.get("salary", {}).get("from", "")
        if item.get("salary") is not None:
            salary_currency = item.get("salary", {}).get("currency", "")

        if item.get("area") is not None:
            area_name = item.get("area", {}).get("name", "")
        if item.get("created_at") is not None:
            created_at = datetime.datetime.strptime(item.get("created_at", ""), "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y %H:%M")
  
        result_list.append({
            "name": name,
            "responsibility": responsibility,
            "requirement": requirement,
            "employer_name": employer_name,
            "salary_from": salary_from,
            "salary_currency": salary_currency,
            "area_name": area_name,
            "created_at": created_at,
        })

    return result_list

def parseCBRF(strCBRF):
    #парсер с апи цб рф
    root = ET.fromstring(strCBRF)

    data_dict = {}
    for item_element in root.findall('.//Valute'):
        CharCode = VunitRate = None
        for child_element in item_element:
            if child_element.tag == 'CharCode':
                CharCode = child_element.text
            elif child_element.tag == 'VunitRate':
                VunitRate = child_element.text

        if CharCode is not None and VunitRate is not None:
            data_dict[CharCode] = VunitRate

    return data_dict

def convertCurrency(listHH, listCBRF):
    for currency, rate in listCBRF.items():
        listCBRF[currency] = float(rate.replace(',', '.'))

    # Корректировка зарплат в вакансиях
    for vacancy in listHH:
        currency = vacancy["salary_currency"]
        if currency in listCBRF:
            rate = listCBRF[currency]
            vacancy["salary_from"] *= rate

    return listHH