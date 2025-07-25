#!/usr/bin/python3

import requests
import warnings
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

def get_information(url, params):
    response = requests.get(url=url, params=params, timeout=10)
    if response.status_code == 200:
        return response.json()

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

def get_clean_data(clean_data):
    required_data = clean_data["Result"]["Resources"]["All"]["Resource"][:30]
    get_all_titles = [data["Title"] for data in required_data]

    all_subtitles = []
    all_resume = []

    for resource in required_data:
        sections = resource["Sections"]["section"]
        subtitles = [section.get("Title", "") for section in sections]
        resume = [section.get("Content", "") for section in sections]
        all_subtitles.extend(subtitles)
        all_resume.extend(resume)

    return get_all_titles, all_subtitles, all_resume

if __name__ == "__main__":
    get_information(url,params)
    strip_html(data)
    get_clean_data(clean_data)
