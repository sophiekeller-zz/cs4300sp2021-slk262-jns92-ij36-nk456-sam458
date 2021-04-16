import jsonlines
import json
from app.irsystem.models.tourpedia_data_structs import city_count

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

# def restaurantMappings():
#   with jsonlines.open('./tokenized-files/london-restaurant.jsonl') as f:
#       line_count = 0
#       restaurantMappings = {}
#       for line in f.iter():
#         name = line["name"]
#         reviews_tokenized = line["reviews_tokenized"]
#         count_dict = {}
#         for category in words:
#           for word in words[category]:
#             if word in reviews_tokenized:
#               if category in count_dict:
#                 count_dict[category] +=1
#               else:
#                 count_dict[category] = 1
#         restaurantMappings[name] = count_dict
#         line_count += 1
#     return restaurantMappings

# with jsonlines.open('app/irsystem/models/tokenized-files/london-restaurant.jsonl') as f:
#     line_count = 0
#     restaurantMappings = {}
#     for line in f.iter():
#       name = line["name"]
#       reviews_tokenized = line["reviews_tokenized"]
#       count_dict = {}
#       for category in restaurant_words:
#         for word in restaurant_words[category]:
#           if word in reviews_tokenized:
#             if category in count_dict:
#               count_dict[category] +=1
#             else:
#               count_dict[category] = 1
#       restaurantMappings[name] = count_dict
#       line_count += 1
#
# with jsonlines.open('app/irsystem/models/tokenized-files/london-accommodation.jsonl') as f:
#     line_count = 0
#     accommodationMappings = {}
#     for line in f.iter():
#       name = line["name"]
#       reviews_tokenized = line["reviews_tokenized"]
#       count_dict = {}
#       for category in accommodation_words:
#         for word in accommodation_words[category]:
#           if word in reviews_tokenized:
#             if category in count_dict:
#               count_dict[category] +=1
#             else:
#               count_dict[category] = 1
#       accommodationMappings[name] = count_dict
#       line_count += 1
def restaurantMatchings(city, query):
  if not query:
    return []
  restaurantDict = {}
  querySet = set(query.split(" "))
  restaurantMappings = city_count[city.lower()]["restaurant"]
  for restaurantName in restaurantMappings:
      words = set(restaurantMappings[restaurantName].keys())
      count = 0
      for category in restaurantMappings[restaurantName]:
        if category in querySet:
          count += restaurantMappings[restaurantName][category] 
      categoriesMet = len(querySet.intersection(words))
      if count > 0:
        restaurantDict[restaurantName] = count
  
  ranked = sorted(restaurantDict.items(), key=lambda x: x[1], reverse=True)
  return ranked[:10]

def accommodationMatchings(city, query):
  if not query:
    return []
  accommodationDict = {}
  querySet = set(query.split(" "))
  accommodationMappings = city_count[city.lower()]["accommodation"]
  for accommodationName in accommodationMappings:
      words = set(accommodationMappings[accommodationName].keys())
      count = 0
      for category in accommodationMappings[accommodationName]:
        if category in querySet:
          count += accommodationMappings[accommodationName][category] 
      categoriesMet = len(querySet.intersection(words))
      if count > 0:
        accommodationDict[accommodationName] = count
  
  ranked = sorted(accommodationDict.items(), key=lambda x: x[1], reverse=True)
  return ranked[:10]

# print(list(restaurantMappings.items())[:10])


