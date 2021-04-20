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

attraction_words = {
  "expensive": ["pricey", "pricy", "expensive"],
  "inexpensive": ["cheap", "inexpensive", "low-cost", "bargain", "affordable"],
  "drinking": ["bar", "pub", "wine", "beer", "shot", "cocktail", "cocktails", "beers"],
  "ambiance": ["setting", "ambiance", "fancy", "pretty", "decor", "decorated", "creative", "vibe", "cute", "vintage"],
  "music": ["music", "pop", "rock", "reggae", "jazz", "band", "performance", "violin", "piano"],
  "sports": ["active", "basketball", "soccer", "tennis", "baseball", "football", "skate", "skating", "lacrosse", "cricket", "rugby", "squash", "yoga", "exercise", "bike", "biking"],
  "water activities": ["pool", "lake", "river", "stream", "ocean", "sea", "beach", "sailing", "sail", "boat", "swim", "swimming"]
}

def get_matchings(city, category, query):

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

def get_matchings_cos_sim(city, category, query):
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
        # categoriesMet = len(querySet.intersection(words))
        if count > 0:
          resultsDict[place] = count
    
    ranked = sorted(resultsDict.items(), key=lambda x: x[1], reverse=True)
    return ranked[:10]


# print(list(restaurantMappings.items())[:10])

def within_rad(city, top_hotels, top_rests, top_attract, radius): # top_attract,
  with open('app/irsystem/models/inverted-index.json') as f:
    inv_ind = json.load(f)
  with open('app/irsystem/models/distance-matrices.json') as f:
    distances = json.load(f)
  within_rad = {}
  for h in top_hotels:
    restaurants = []
    for r in top_rests:
      dist = distances[city]['restaurant'][inv_ind[city]['restaurant'][r]][inv_ind[city]['accommodation'][h]]
      if dist <= radius:
        restaurants.append(r)
    attractions = []
    for a in top_attract:
      dist = distances[city]['attraction'][inv_ind[city]['attraction'][a]][inv_ind[city]['accommodation'][h]]
      if dist <= radius:
        attractions.append(a)
    within_rad[h] = {'restaurants': restaurants,'attractions': attractions }

  return within_rad

#rests = getMatchings('london', 'accommodation', 'clean');
# hots =  getMatchings('london', 'accommodation', 'clean');
# print(list(withinRad('london',hots, rests, 10000000)));