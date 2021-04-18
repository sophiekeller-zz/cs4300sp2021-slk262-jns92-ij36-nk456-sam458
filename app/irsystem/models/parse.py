# import requests
# import json
# import csv


# places = requests.get(
#     f"http://tour-pedia.org/api/getPlaces?category=restaurant&location={city}").json()



for city in ["london","amsterdam", "barcelona", "berlin", "dubai"]:
    for category in ["accommodation", "restaurant", "attraction"]:
        print(f"starting {category}")
        with open(f"tourpedia_files/{city}-{category}.csv") as csvfile:
            csvReader = csv.DictReader(csvfile)
            for row in csvReader:
                if row["reviews"] is not None:
                    place = {"name": row["name"],"lat":row["lat"], "lng":row["lng"], "address": row["address"]}
                    if "subCategory" in row:
                        place["subCategory"] = row["subCategory"]
                    try: 
                        reviews = requests.get(row["reviews"]).json()
                        pared_reviews = []
                        for r in reviews:
                            pared_reviews.append({"language": r["language"], "rating": r["rating"], "text":r["text"]})
                        if pared_reviews:
                            place["reviews"] = pared_reviews
                            with open(f'{city}-{category}.jsonl', 'a') as outfile:
                                json.dump(place, outfile) 
                                outfile.write("\n")
                    except Exception as e:
                        pass
                
        

