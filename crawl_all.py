"""
Hauptprogramm, dass
 - Alle Postleitzahlen für Städte abfragt
 - Alle Tankstellen je Postleitzahl ermittelt
 - Für alle Tankstellen die 1 Wochen-Historie der Spritpreise ermittelt
 - Das ergebnis als gzipped JSON speichert
"""
import plz_crawler
import tankstellen_crawler
import spritpreis_crawler
import store

plz_set = plz_crawler.get_plz_set(0, 2, 100)
tankstellen_links = tankstellen_crawler.get_links_for_plz_set(plz_set, 16)
spritpreis_daten = spritpreis_crawler.get_data_for_tankstellen_set(tankstellen_links, 16)

store.save_data("station_data.json.gz", spritpreis_daten)
