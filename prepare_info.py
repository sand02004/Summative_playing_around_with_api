#!/usr/bin/python3

import requests
import warnings
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

params = {
    "age": 25,
    "sex": "female",
    "pregnant": "yes",
    "sexually active": "yes",
    "tobaccouse": "no"
}

url = "https://odphp.health.gov/myhealthfinder/api/v4/myhealthfinder.json"

def get_information(url, params):
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        return response.json()

data = get_information(url, params)

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

def strip_html(data):
    if isinstance(data, str):
        return BeautifulSoup(data, "html.parser").get_text()
    elif isinstance(data, list):
        return [strip_html(item) for item in data]
    elif isinstance(data, dict):
        return {key: strip_html(value) for key, value in data.items()}
    else:
        return data

clean_data = strip_html(data)

def get_clean_data(clean_data):
    required_data = clean_data["Result"]["Resources"]["All"]["Resource"][:5]
    get_all_titles = [data["Title"] for data in required_data]

    all_subtitles = []
    all_resume = []

    for resource in required_data:
        sections = resource["Sections"]["section"]
        subtitles = [section.get("Title", "") for section in sections]
        resume = [section.get("Content", "") for section in sections]
        all_subtitles.extend(subtitles)
        all_resume.extend(resume)

    ressource_url = "https://odphp.health.gov/myhealthfinder/pregnancy/doctor-and-midwife-visits/have-healthy-pregnancy"
    url_list = [ressource_url] * 20
    return get_all_titles, all_subtitles, all_resume

