import jsonlines
import json
# import matplotlib.pyplot as plt

dirty_words = 0
clean_words = 0
loud_words = 0
quiet_words = 0
positive_words = 0
negative_words = 0
water_words = 0


words = {
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

words = {
  "good taste": ["delicious", "delectable", "fresh", "tasty", "yum", "yummy", "flavorful", "divine", "good", "nice", "kind", "perfect", "great", "lovely", "beautiful", "perfect", "amazing", "brilliant", "incredible", "fantastic", "pleasant", "wonderful", "comfortable", "best", "bright", "greatest"],
  "bad taste": ["bad", "worst", "wait", "unpleasant", "gross", "dirty", "yuck", "dry", "under", "raw", "undercooked", "rot", "rotten"],
  "expensive": ["pricey", "pricy", "expensive"],
  "inexpensive": ["cheap", "inexpensive", "low-cost", "bargain", "affordable"],
  "drinking": ["bar", "pub", "wine", "beer", "shot", "cocktail", "cocktails", "beers"],
  "ambiance": ["setting", "ambiance", "fancy", "pretty", "decor", "decorated", "creative", "vibe", "cute", "vintage"],
  "music": ["music", "pop", "rock", "reggae", "jazz", "band", "performance"]
}

words = {
  "expensive": ["pricey", "pricy", "expensive"],
  "inexpensive": ["cheap", "inexpensive", "low-cost", "bargain", "affordable"],
  "drinking": ["bar", "pub", "wine", "beer", "shot", "cocktail", "cocktails", "beers"],
  "ambiance": ["setting", "ambiance", "fancy", "pretty", "decor", "decorated", "creative", "vibe", "cute", "vintage"],
  "music": ["music", "pop", "rock", "reggae", "jazz", "band", "performance", "violin", "piano"],
  "sports": ["active", "basketball", "soccer", "tennis", "baseball", "football", "skate", "skating", "lacrosse", "cricket", "rugby", "squash", "yoga", "exercise", "bike", "biking"],
  "water activities": ["pool", "lake", "river", "stream", "ocean", "sea", "beach", "sailing", "sail", "boat", "swim", "swimming"]

}

counts = {category: 0 for category in words}

# for city in ["london","amsterdam", "barcelona", "berlin", "dubai"]:
#     for category in ["accommodation", "restaurant", "attraction"]:
#         with jsonlines.open(f"jsonl-files/{city}-{category}.jsonl") as f:
#           for line in f.iter():
#             tokens = []
#             for r in line["reviews"]:
#               tokens += [x.lower() for x in r["text"].split(" ")]
#             line["reviews_tokenized"] = tokens
#             with open(f'tokenized-files/{city}-{category}.jsonl', 'a') as outfile:
#               json.dump(line, outfile) 
#               outfile.write("\n")

tokens_mapping = {}
for city in ["london","amsterdam", "barcelona", "berlin", "dubai"]:
    category_map = {}
    for category in ["accommodation", "restaurant", "attraction"]:
        tokens_map = {}
        with jsonlines.open(f'tokenized-files/{city}-{category}.jsonl') as f:
          for line in f.iter():
            stringified = ""
            for token in line["reviews_tokenized"]:
              stringified += token + " "
            tokens_map[line["name"]] = stringified

        category_map[category] = tokens_map
    tokens_mapping[city] = category_map

with open('tokens_mapping.json','a') as out:
  json.dump(tokens_mapping, out)
  out.write("\n")

# with jsonlines.open('london-attraction.jsonl') as f:
#     line_count = 0
#     for line in f.iter():
#       reviews = line["reviews"]
#       for category in words:
#         for word in words[category]:
#           if word in reviews:
#             counts[category] += 1
#       line_count += 1

# pairs = counts.items()
# keys = [x[0] for x in pairs]
# vals = [x[1] for x in pairs]
# plt.title("London Attraction Review Categories")
# plt.ylabel('Amounts')
# plt.xlabel('Word Category')
# plt.bar(keys, vals)
# plt.show()

# print(f"{line_count} hotels reviewed")
# for category in counts:
#   print(f"{counts[category]} hotels received reviews corresponding to {category}")