import jsonlines
import json

words = {
  "good taste": ["delicious", "delectable", "fresh", "tasty", "yum", "yummy", "flavorful", "divine", "good", "nice", "kind", "perfect", "great", "lovely", "beautiful", "perfect", "amazing", "brilliant", "incredible", "fantastic", "pleasant", "wonderful", "comfortable", "best", "bright", "greatest"],
  "bad taste": ["bad", "worst", "wait", "unpleasant", "gross", "dirty", "yuck", "dry", "under", "raw", "undercooked", "rot", "rotten"],
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

with jsonlines.open('./tokenized-files/london-restaurant.jsonl') as f:
    line_count = 0
    restaurantMappings = {}
    for line in f.iter():
      name = line["name"]
      reviews_tokenized = line["reviews_tokenized"]
      count_dict = {}
      for category in words:
        for word in words[category]:
          if word in reviews_tokenized:
            if category in count_dict:
              count_dict[category] +=1
            else:
              count_dict[category] = 1
      restaurantMappings[name] = count_dict
      line_count += 1
  

def restaurantMatchings(query):
  restaurantList = []
  querySet = set([query])
  for restaurantName in restaurantMappings:
      words = set(restaurantMappings[restaurantName].keys())
      if(querySet.issubset(words)):
        restaurantList.append(restaurantName)
  return restaurantList

# print(list(restaurantMappings.items())[:10])


