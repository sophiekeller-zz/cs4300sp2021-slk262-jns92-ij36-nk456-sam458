import jsonlines

city_count = {}

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
    for m in maps:
        json_string = 'app/irsystem/models/tokenized-files/'+c+'-'+m+'.jsonl'
        with jsonlines.open(json_string) as f:
            line_count = 0
            mappings = {}
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
                line_count += 1
        city_count[c][m] = mappings

