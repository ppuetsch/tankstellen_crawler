"""
Speichert die Daten, die tankstellen_crawler extrehiert hat,
in station_data.json.gz (stammdaten) und timestamp.gz (marktdaten)
"""
import time
import json
import gzip


def save_data(station_data_filename, spritpreis_daten):
    added = 0
    modified = 0
    deleted = 0
    history_only = {link: {"history": details["history"], "timestamp": details["timestamp"]}
                    for (link, details) in spritpreis_daten.items()}
    print("History extracted")
    filename = "{}".format(time.time()) + ".json.gz"
    with gzip.open(filename, 'wt', encoding="ascii") as outfile:
        json.dump(history_only, outfile)
    print("History dumped")
    try:
        with gzip.open(station_data_filename, 'rt', encoding='ascii') as infile:
            old_station_data = json.load(infile)
    except FileNotFoundError:
        old_station_data = {}
    print("Old data loaded")
    station_data = {link: {details["timestamp"]: details["station_data"]}
                    for (link, details) in spritpreis_daten.items()}
    print("Station Data extracted")

    for link in old_station_data.keys():
        if link not in station_data:
            max_available_ts = max(old_station_data[link].keys())
            old_station_data[link][max_available_ts]["deleted"] = "deleted"
            deleted += 1
    print("Deleted: ", deleted)

    for link, station_detail in station_data.items():
        if link in old_station_data:
            max_available_ts = max(old_station_data[link].keys())
            if old_station_data[link][max_available_ts] != list(station_detail.values())[0]:
                old_station_data[link][list(station_detail.keys())[0]] = station_detail.values()[0]
                modified += 1
        else:
            old_station_data[link] = station_detail
            added += 1
    print("Modified: ", modified)
    print("Added: ", added)
    with gzip.open(station_data_filename, 'wt', encoding='ascii') as outfile:
        json.dump(old_station_data, outfile)
