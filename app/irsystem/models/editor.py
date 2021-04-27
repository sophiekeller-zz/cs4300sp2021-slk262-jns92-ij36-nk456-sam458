import json
from PyDictionary import PyDictionary

with open('tokens_mapping.json') as f:
  mapping = json.load(f)

negation_words = set(["no", "not", "none", "nothing", "neither", "nowhere", "never", "hardly", "barely"])
dictionary=PyDictionary()

def negate_words(review_words):
  ind = 0
  while ind < len(review_words) - 1:
    if review_words[ind] in negation_words:
      del review_words[ind]
      ants = dictionary.antonym(review_words[ind])
      if ants:
        review_words[ind] = dictionary.antonym(review_words[ind])[0]
      else:
        del review_words[ind]
        ind -= 1
    ind += 1
  return " ".join(review_words)

negation_mapping = {}
for city in mapping:
    print(city)
    category_map = {}
    for category in mapping[city]:
        print(category)
        tokens_map = {}
        for place in mapping[city][category]:
          review_words = mapping[city][category][place].split(" ")
          tokens_map[place] = negate_words(review_words)
        category_map[category] = tokens_map
    negation_mapping[city] = category_map

with open('negation_mapping.json','a') as out:
  json.dump(negation_mapping, out)
  out.write("\n")