# import jsonlines
import nltk
from nltk.corpus import wordnet
import json
import math
# from app.irsystem.models.tourpedia_data_structs import city_count, city_ind
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

accommodation_words = {
    "dirty": ["stink", "stinks", "smells", "stinky", "rotten", "disgusting", "gross", "nasty", "worn", "dirty"],
    "clean": ["flawless", "clean", "clear", "comfortable", "comfortably"],
    "loud": ["loud", "noise", "noisy"],
    "quiet": ["quiet"],
    # "positive": ["good", "nice", "kind", "perfect", "great", "lovely", "beautiful", "perfect", "amazing", "brilliant", "incredible", "fantastic", "pleasant", "wonderful", "comfortable", "best", "bright", "greatest"],
    "negative": ["bad", "worst", "wait", "unpleasant"],
    "swimming": ["sauna", "pool", "spa", "swim", "swimming", "ocean", "lake"],
    "nature": ["garden", "park", "river", "lake", "sunset"],
    "expensive": ["pricey", "pricy", "expensive"],
    "inexpensive": ["cheap", "inexpensive", "low-cost", "bargain", "affordable"],
    "drinking": ["bar", "pub"]
}

restaurant_words = {
    "good-taste": ["delicious", "delectable", "fresh", "tasty", "yum", "yummy", "flavorful", "divine", "good", "nice",
                   "kind", "perfect", "great", "lovely", "beautiful", "perfect", "amazing", "brilliant", "incredible",
                   "fantastic", "pleasant", "wonderful", "comfortable", "best", "bright", "greatest"],
    "bad-taste": ["bad", "worst", "wait", "unpleasant", "gross", "dirty", "yuck", "dry", "under", "raw", "undercooked",
                  "rot", "rotten"],
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
    "sports": ["active", "basketball", "soccer", "tennis", "baseball", "football", "skate", "skating", "lacrosse",
               "cricket", "rugby", "squash", "yoga", "exercise", "bike", "biking"],
    "water activities": ["pool", "lake", "river", "stream", "ocean", "sea", "beach", "sailing", "sail", "boat", "swim",
                         "swimming"]
}
map_words = {
    "restaurant": restaurant_words, "accommodation": accommodation_words, "attraction": attraction_words}

negation_words = ["no", "not", "none", "nothing", "neither", "nowhere", "never", "hardly", "barely"]


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


def build_vectorizer(max_n_terms=5000, max_prop_docs=0.8, min_n_docs=0):
    """Returns a TfidfVectorizer object with certain preprocessing properties.
    
    Params: {max_n_terms: Integer,
             max_prop_docs: Float,
             min_n_docs: Integer}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(min_df=min_n_docs, max_df=max_prop_docs, max_features=max_n_terms,
                           stop_words='english')


# def get_query_antonyms(query):
#     antonyms = []
#     for q in query.split(" "):
#         for syn in wordnet.synsets(q):
#             found_ant = False
#             for l in syn.lemmas():
#                 if l.antonyms() and not found_ant:
#                     found_ant = True
#                     antonyms.append(l.antonyms()[0].name())
#
#     return antonyms


def get_cos_sim(query, reviews, q):
    """Returns the cosine similarity of two movie scripts.
    
    Params: {mov1: String,
             mov2: String,
             input_doc_mat: np.ndarray,
             movie_name_to_index: Dict}
    Returns: Float 
    """
    numerator = np.dot(query, reviews)
    #query_antonyms = get_query_antonyms(q)
    tfidf_vec = build_vectorizer()
    #numerator_negative = np.dot(tfidf_vec.fit_transform(query_antonyms).toarray(), reviews)
    denomenator = (np.linalg.norm(query) * np.linalg.norm(reviews))
    #if numerator - numerator_negative == 0 or denomenator == 0:
    if numerator == 0 or denomenator == 0:
        return 0.0
    #return (numerator - numerator_negative) / (np.linalg.norm(query) * np.linalg.norm(reviews))
    return numerator/ (np.linalg.norm(query) * np.linalg.norm(reviews))


def get_matchings_cos_sim(city, category, query):
    with open('app/irsystem/models/tokens_mapping.json') as f:
        tokens_map = json.load(f)
        if not query:
            print("NO QUERY")
            return []

        # get query string/vector
        related_words = []
        for query in query.split(" "):
          try:
            print(query)
            related_words += map_words[category][query]
          except:
            print(query)
            related_words = related_words
        query_string = " ".join(related_words)

        # list of all review strings (each place has a single review string of all reviews) with
        # the query string as the last vector
        to_vectorize = [tokens_map[city][category][x] for x in tokens_map[city][category]] + [query_string]
        tfidf_vec = build_vectorizer()
        tfidf_mat = tfidf_vec.fit_transform(to_vectorize).toarray()

        # calculate cosine sims between each place's tf-idf vector and the query string vector
        cos_sims = [get_cos_sim(tfidf_mat[i], tfidf_mat[-1], query) for i in range(len(tfidf_mat - 1))]
        sims_idx = [(i, sim) for i, sim in enumerate(cos_sims)]
        ranked = sorted(sims_idx, key=lambda x: x[1], reverse=True)[1:]  # slice off query

        # translate from id's to names
        keys = list(tokens_map[city][category].keys())
        ranked_translated = [(keys[x[0]], x[1]) for x in ranked]

        return ranked_translated[:10]


# print(list(restaurantMappings.items())[:10])

def within_rad(city, top_hotels, top_rests, top_attract, radius):  # top_attract,
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
        within_rad[h] = {'restaurants': restaurants, 'attractions': attractions}

    return within_rad

# rests = getMatchings('london', 'accommodation', 'clean');
# hots =  getMatchings('london', 'accommodation', 'clean');
# print(list(withinRad('london',hots, rests, 10000000)));
