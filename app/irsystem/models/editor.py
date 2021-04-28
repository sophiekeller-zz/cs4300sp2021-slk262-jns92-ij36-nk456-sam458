import json
from PyDictionary import PyDictionary
import nltk
from nltk import PorterStemmer

porter = PorterStemmer()

with open('tokens_mapping.json') as f:
  mapping = json.load(f)

negation_words = set(["no", "not", "none", "nothing", "neither", "nowhere", "never", "hardly", "barely"])
dictionary=PyDictionary()

# def negate_words(review_words):
#   ind = 0
#   while ind < len(review_words) - 1:
#     if review_words[ind] in negation_words:
#       del review_words[ind]
#       ants = dictionary.antonym(review_words[ind])
#       if ants:
#         review_words[ind] = dictionary.antonym(review_words[ind])[0]
#       else:
#         del review_words[ind]
#         ind -= 1
#     ind += 1
#   return " ".join(review_words)

# negation_mapping = {}
# for city in mapping:
#     print(city)
#     category_map = {}
#     for category in mapping[city]:
#         print(category)
#         tokens_map = {}
#         for place in mapping[city][category]:
#           review_words = mapping[city][category][place].split(" ")
#           tokens_map[place] = negate_words(review_words)
#         category_map[category] = tokens_map
#     negation_mapping[city] = category_map

# with open('negation_mapping.json','a') as out:
#   json.dump(negation_mapping, out)
#   out.write("\n")

def stem_sentence(sentence): 
  tokens = sentence.split(" ")
  stemmed_sentence = ""
  for tok in tokens: 
    stemmed_sentence += porter.stem(tok) + " "
  return stemmed_sentence


stemmed_mapping = mapping.copy()
for city in mapping:
  for category in mapping[city]:
    for place in mapping[city][category]:
      stemmed = stem_sentence(mapping[city][category][place])
      stemmed_mapping[city][category][place] = stemmed

print(len(stemmed_mapping))

with open('stemmed_mapping.json', 'a') as out:
  json.dump(stemmed_mapping, out)
  out.write("\n")
