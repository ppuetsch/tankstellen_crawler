import requests_html
import re
from multiprocessing.pool import ThreadPool



def get_links_for_plz(plz="51429"):
    with requests_html.HTMLSession() as session:
        print("Crawling Tankstellen Links für PLZ {}".format(plz))
        matcher = re.compile("https://mehr-tanken.de/tankstelle/......../")
        request_params = {"searchText": plz}
        r = session.get("https://mehr-tanken.de/tankstellen", params=request_params)
        return {link for link in r.html.absolute_links if matcher.match(link)}


def get_links_for_plz_set(plz_set=None, max_concurrent_requests=8):
    if plz_set == None:
        plz_set={"51429"}
    print("Crawling {} Postleitahlen nach Tankstellen".format(len(plz_set)))
    link_set = set()
    linkSets = ThreadPool(max_concurrent_requests).map(get_links_for_plz, plz_set)
    for small_link_set in linkSets:
        link_set.update(small_link_set)
    return link_set
