# import jsonlines
import json
# from app.irsystem.models.tourpedia_data_structs import city_count, city_ind


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
def getMatchings(city, category, query):

  with open('app/irsystem/models/mappings.json') as f:
    city_count = json.load(f)
    if not query:
      return []
    resultsDict = {}
    querySet = set(query.split(" "))
    mappings = city_count[city.lower()][category]
    for place in mappings:
        words = set(mappings[place].keys())
        count = 0
        for category in mappings[place]:
          if category in querySet:
            count += mappings[place][category] 
        categoriesMet = len(querySet.intersection(words))
        if count > 0:
          resultsDict[place] = count
    
    ranked = sorted(resultsDict.items(), key=lambda x: x[1], reverse=True)
    return ranked[:10]


# print(list(restaurantMappings.items())[:10])

def withinRad(city, top_hotels, top_rests, radius): # top_attract,
  fh = open('/app/irsystem/models/inverted-index.json', 'r')
  inv_ind = fh.readlines()
  fh.close()
  fh = open('/app/irsystem/models/distance-matrices.json', 'r')
  distances = fh.readlines()
  fh.close()
  within_rad = {}
  for h in top_hotels:
    restaurants = []
    for r in top_rests:
      dist = distances[city][inv_ind[city]['accommodation'][h]][inv_ind[city]['restaurant'][r]]
      if dist <= radius:
        restaurants.append(r)
    # attracts = []
    # for a in top_attract:
    #   dist = distances[city][inv_ind[city]['accommodation'][h]][inv_ind[city]['attraction'][a]]
    #   if dist <= radius:
    #     attracts.append(a)
    within_rad[h] = {'restaurants': restaurants}#,'attractions':attractions

  return within_rad

# rests = getMatchings('london', 'accommodation', 'clean');
# hots =  getMatchings('london', 'accommodation', 'clean');
# print(list(withinRad('london',hots, rests, 10000000)));