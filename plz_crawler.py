"""
Fragt alle zugewiesenen Postleitzahlen, die "Städten" zugeordnet sind, ab.
Hierzu wird die Seite "www.postdirekt.de/plzserver/" verwendet.
"""

import requests
from multiprocessing.pool import ThreadPool


def request_for_plz_area(plz_area):
    "Fragt alle Postleitzahlen für ein Postleitzahlgebiet (z.B. '50') ab und gibt das Ergebnis als JSON entsprechend dem Format von postdirekt.de zurück"
    url = "https://www.postdirekt.de/plzserver/PlzAjaxServlet".format(50)
    payload = {'nocache': '559982368047', 'finda': 'city', 'city': "{:02d}".format(plz_area)}
    return requests.get(url, params=payload)


def get_plz_set(start_area=0, end_area=100, max_concurrent_requests=8):
    "Fragt alle Postleitzahlen für eine Range von Postleitzahlgebieten (z.B. '40'-'50') ab und gibt das Ergebnis als Set zurück"
    plz_set = set()

    request_results = ThreadPool(max_concurrent_requests).map(request_for_plz_area, range(start_area, end_area))
    for r in request_results:
        if r.status_code != 200:
            continue
        if 'rows' in r.json():
            for row in r.json()['rows']:
                plz_set.add(row['plz'])
        else:
            print(r.text)
    print("Postleitzahlen erfolgreich empfangen")
    return plz_set
