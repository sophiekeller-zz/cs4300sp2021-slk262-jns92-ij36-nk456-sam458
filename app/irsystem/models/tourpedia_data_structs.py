import jsonlines
# import numpy as np
# import math
import json
city_count = {}
city_coords = {}

accommodation_words = {
  "dirty": ["stink", "stinks", "smells", "stinky", "rotten", "disgusting", "gross","nasty", "worn", "dirty"],
  "clean": ["flawless", "clean", "clear", "comfortable", "comfortably"],
  "loud": ["loud", "noise", "noisy"],
  "quiet": ["quiet"],
  #"positive": ["good", "nice", "kind", "perfect", "great", "lovely", "beautiful", "perfect", "amazing", "brilliant", "incredible", "fantastic", "pleasant", "wonderful", "comfortable", "best", "bright", "greatest"],
  "negative": ["bad", "worst", "wait", "unpleasant"],
  "swimming": ["sauna", "pool", "spa", "swim", "swimming", "ocean", "lake"],
  "nature": ["garden", "park", "river", "lake", "sunset"],
  "expensive": ["pricey", "pricy", "expensive"],
  "inexpensive": ["cheap", "inexpensive", "low-cost", "bargain", "affordable"],
  "drinking": ["bar", "pub"]
}

restaurant_words = {
  "good-taste": ["delicious", "delectable", "fresh", "tasty", "yum", "yummy", "flavorful", "divine", "good", "nice", "kind", "perfect", "great", "lovely", "beautiful", "perfect", "amazing", "brilliant", "incredible", "fantastic", "pleasant", "wonderful", "comfortable", "best", "bright", "greatest"],
  "bad-taste": ["bad", "worst", "wait", "unpleasant", "gross", "dirty", "yuck", "dry", "under", "raw", "undercooked", "rot", "rotten"],
  "expensive": ["pricey", "pricy", "expensive"],
  "inexpensive": ["cheap", "inexpensive", "low-cost", "bargain", "affordable"],
  "drinking": ["bar", "pub", "wine", "beer", "shot", "cocktail", "cocktails", "beers"],
  "ambiance": ["setting", "ambiance", "fancy", "pretty", "decor", "decorated", "creative", "vibe", "cute", "vintage"],
  "music": ["music", "pop", "rock", "reggae", "jazz", "band", "performance"]
}

cities = ["berlin", "barcelona", "dubai", "london", "amsterdam"]
maps = ["restaurant", "accommodation"]
words = {"restaurant": restaurant_words, "accommodation": accommodation_words}
ind = 0
for c in cities:
    city_count[c] = {}
    city_coords[c] = {}
    for m in maps:
        json_string = 'tokenized-files/'+c+'-'+m+'.jsonl'
        with jsonlines.open(json_string) as f:
            line_count = 0
            mappings = {}
            coords = {}
            for line in f.iter():
                name = line["name"]
                reviews_tokenized = line["reviews_tokenized"]
                count_dict = {}
                for category in words[m]:
                    for word in words[m][category]:
                        if word in reviews_tokenized:
                            if category in count_dict:
                                count_dict[category] += 1
                            else:
                                count_dict[category] = 1
                mappings[name] = count_dict
                coords[name] = {"lat": line["lat"], "lng": line["lng"]}
                line_count += 1
        city_coords[c][m] = coords
        city_count[c][m] = mappings
    
# with open('mappings.json', 'a') as outfile:
#     json.dump(city_count, outfile) 

#inverted indices 
city_ind = {}
for c in cities:
    city_ind[c] = {}
    for m in maps:
        ind = 0
        index = {}
        for i in city_count[c][m]:
            index[i] = ind
            ind += 1
        city_ind[c][m] = index

# with open('inverted-index.json', 'a') as outfile:
#     json.dump(city_ind, outfile) 

#formula found @ http://www.movable-type.co.uk/scripts/latlong.html
def distance_between(lat1, lat2, long1, long2):
    lat1, lat2, long1, long2 = float(lat1), float(lat2), float(long1), float(long2)
    phi1 = lat1 * math.pi / 180 #radians
    phi2 = lat2 * math.pi / 180
    change_lat = (lat2 - lat1) * math.pi / 180
    change_long = (long2 - long1) * math.pi / 180
    a = math.sin(change_lat / 2) * math.sin(change_lat / 2) + math.cos(phi1) * \
        math.cos(phi2) * math.sin(change_long / 2) * math.sin(change_long / 2)
    dist = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371e3 * dist #in meters


#distance matrices
city_dist = {}
for c in cities:
    mat = np.zeros((len(city_count[c]["restaurant"]), len(city_count[c]["accommodation"])))
    for r in city_count[c]["restaurant"]:
        for a in city_count[c]["accommodation"]:
            ind_r = city_ind[c]["restaurant"][r]
            ind_a = city_ind[c]["accommodation"][a]
            mat[ind_r][ind_a] = distance_between(city_coords[c]['restaurant'][r]["lat"],
                                                 city_coords[c]['accommodation'][a]["lat"],
                                                 city_coords[c]['restaurant'][r]["lng"],
                                                 city_coords[c]['accommodation'][a]["lng"])
    city_dist[c] = mat.tolist()

with open('distance-matrices.json', 'a') as outfile:
    json.dump(city_dist, outfile) 