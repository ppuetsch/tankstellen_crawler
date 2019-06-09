import requests
from multiprocessing.pool import ThreadPool


def request_for_plz(plz):
    url = "https://www.postdirekt.de/plzserver/PlzAjaxServlet".format(50)
    payload = {'nocache': '559982368047', 'finda': 'city', 'city': "{:02d}".format(plz)}
    return requests.get(url, params=payload)


def get_plz_set(start=0, end=100, max_concurrent_requests=8):
    plz_set = set()

    request_results = ThreadPool(max_concurrent_requests).map(request_for_plz, range(start, end))
    for r in request_results:
        if r.status_code != 200:
            continue
        if 'rows' in r.json():
            for row in r.json()['rows']:
                plz_set.add(row['plz'])
        else:
            print(r.text)
    print("PLZ erfolgreich empfangen")
    return plz_set
