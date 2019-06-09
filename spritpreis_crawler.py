import requests_html
import urllib.parse
import json
from multiprocessing.pool import ThreadPool
import time


def get_data_for_tankstellen_link(
        link="https://mehr-tanken.de/tankstelle/dbc87db1/shell-karl-krekeler-str-2-51373-leverkusen"):
    print("Crawling Tankdaten für Link {}".format(link))
    result = {}
    history = {}
    result['timestamp'] = time.time()
    try:
        full_link = urllib.parse.urljoin(link, "e5")
        session = requests_html.HTMLSession()
        r = session.get(full_link)
    except:
        print("Could not load data from URL {}. Passing silently", link)
    try:
        result['station_data'] = json.loads(r.html.find("chart", first=True).attrs["station-data"])
    except:
        result['station_data'] = "station_data not found"
    try:
        statistics_data = json.loads(r.html.find("chart", first=True).attrs["statistics-data"])[0]["data"]
        for (sorte, daten) in statistics_data.items():
            for datum in daten["chartData"]:
                if datum['name'] == 'Preise letzte Woche':
                    history[sorte] = datum['values']
        result['history'] = history
    except:
        result['history'] = "No history data found"
    return link, result

def get_data_for_tankstellen_set(
        links=None,
        max_concurrent_requests=8):
    if links==None:
        links = {"https://mehr-tanken.de/tankstelle/dbc87db1/shell-karl-krekeler-str-2-51373-leverkusen"}
    print("Crawling {} Tankstellen nach Daten".format(len(links)))
    return {link: data for (link, data) in
            ThreadPool(max_concurrent_requests).map(get_data_for_tankstellen_link, links)}
