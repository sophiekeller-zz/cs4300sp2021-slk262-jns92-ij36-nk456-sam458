import requests
import json
import csv

city = "london"
category = "restaurant"
for city in ["london","amsterdam", "barcelona", "berlin", "dubai"]:
    print(f"starting {city}")
    for category in ["accommodation", "restaurant", "attraction"]:
        print(f"starting {category}")
        sites = {}
        with open(f"tourpedia_files/{city}-{category}.csv") as csvfile:
            csvReader = csv.DictReader(csvfile)
            count = 0
            for row in csvReader:
                count += 1
                if count%100 == 0:
                    print(count)
                name = row['name']
                # print(name)
                if row['details'] is not None: 
                    try: 
                        details = requests.get(row["details"]).json()
                        sites[name] = details['external_urls']['Foursquare']
                    except Exception as e:
                        pass
        with open(f'{city}-{category}-sites.jsonl', 'a') as out:
            json.dump(sites, out)
            out.write("\n") 
        print(f"finished {city} {category}")
        