import pickle
import jsonlines
import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()
# from nltk.corpus import wordnet
import json
import math
from PyDictionary import PyDictionary
import numpy.linalg as LA

import numpy as np
import word_forms
from word_forms.word_forms import get_word_forms
# import app.irsystem.models.vectorizer as precomp

# from nltk import PorterStemmer

# porter = PorterStemmer()

dictionary=PyDictionary()



def get_query_antonyms(query):
    antonyms = []
    synonyms = []
    for q in query.split(" "):
        syn = dictionary.synonym(q)
        if not syn:
            synonyms += [q]
        else:
            synonyms += syn[:10] + [q]
        if dictionary.antonym(q):
            antonyms += dictionary.antonym(q)[:10]
    # print(synonyms)
    antonyms = " ".join(antonyms)
    synonyms = " ".join(synonyms) 

    return antonyms, synonyms

def find_word_forms(word): 
    dic = get_word_forms(word)
    words = "" 
    for form in dic: 
        for w in dic[form]: 
            words += w + " "
    return words

def many_word_forms(query): 
    words = "" 
    query = query.split(" ")
    for tok in query: 
        words += find_word_forms(tok)
    return words


def get_cos_sim(query, reviews):
    """Returns the cosine similarity of two movie scripts.
    
    Params: {mov1: String,
             mov2: String,
             input_doc_mat: np.ndarray,
             movie_name_to_index: Dict}
    Returns: Float 
    """
    numerator = np.dot(query, reviews)
    denomenator = (np.linalg.norm(query) * np.linalg.norm(reviews))
    if numerator == 0 or denomenator == 0:
        return 0.0
    return numerator/ (np.linalg.norm(query) * np.linalg.norm(reviews))

def cosineSim(city, category, query):
    with open('app/irsystem/models/tokens_mapping.json') as f:
        tokens_map = json.load(f)
    with open('app/irsystem/models/ranking_mapping.json') as f:
        rankings_map = json.load(f)
    if not query:
        return sorted(rankings_map[city][category].items(), key=lambda x: x[1], reverse=True)

    vec = pickle.load(open(f"app/irsystem/models/pickle/vec-{city}-{category}.pickle", "rb"))
    doc_vectorizer_array = pickle.load(open(f"app/irsystem/models/pickle/vec-array-{city}-{category}.pickle", "rb")).toarray()
    reverse_index = pickle.load(open(f"app/irsystem/models/pickle/reverse-{city}-{category}.pickle", "rb"))
    svd = pickle.load(open(f"app/irsystem/models/pickle/svd-dict-{city}-{category}.pickle", "rb"))

    query_antonyms, query_synonyms = get_query_antonyms(query)
    
    synonyms_forms = many_word_forms(query_synonyms).split(" ")
    antonyms_forms = many_word_forms(query_antonyms).split(" ")

    query_vectorizer_array = np.zeros((doc_vectorizer_array.shape[1],))
    ants_vectorizer_array = np.zeros((doc_vectorizer_array.shape[1],))
    
    for w in synonyms_forms:
        idx = reverse_index.get(w, -1)

        if idx > 0:
            query_vectorizer_array[idx] += 1.0
    
    for w in antonyms_forms:
        idx = reverse_index.get(w, -1)
        if idx > 0:
            ants_vectorizer_array[idx] += 1.0

    query_vectorizer_array *= vec.idf_
    ants_vectorizer_array *= vec.idf_
    
    if query_vectorizer_array.sum() == 0:
        return sorted(rankings_map[city][category].items(), key=lambda x: x[1], reverse=True)

    u,s,v_t = svd
    k = int(0.6 * v_t.shape[0]) # 500
    q = query_vectorizer_array
    q_hat = np.matmul(np.transpose(u[:,:k]),q)

    sim = []
    for i in range(doc_vectorizer_array.shape[0]):
        num = np.matmul(np.matmul(np.diag(s[:k]),v_t[:k,i]),np.transpose(q_hat))
        denom = np.linalg.norm(np.matmul(np.diag(s[:k]),v_t[:k,i]))*np.linalg.norm(q_hat)
        sim.append(num/denom)

    q = ants_vectorizer_array
    q_hat = np.matmul(np.transpose(u[:,:k]),q)

    sim2 = []
    for i in range(doc_vectorizer_array.shape[0]):
        num = np.matmul(np.matmul(np.diag(s[:k]),v_t[:k,i]),np.transpose(q_hat))
        denom = np.linalg.norm(np.matmul(np.diag(s[:k]),v_t[:k,i]))*np.linalg.norm(q_hat)
        sim2.append(num/denom)


    # print(doc_vectorizer_array.shape[0])
    # for i in range(doc_vectorizer_array.shape[0]):
    #     num_syn = np.matmul(query_vectorizer_array, svd_dict)
    #     num_ant = np.matmul(ants_vectorizer_array, svd_dict)
    #     denom_syn = np.linalg.norm(num_syn) * np.linalg.norm(svd_dict)
    #     denom_ant = np.linalg.norm(num_ant) * np.linalg.norm(svd_dict)
    #     sim_syn.append(num_syn/denom_syn)
    #     sim_ant.append(num_ant/denom_ant)
    # doc_vectorizer_array = inverse_transform(svd_dict)
    # print("doc vect shape", doc_vectorizer_array.shape)

    
    # num = query_vectorizer_array.dot(doc_vectorizer_array.T)
    # denom = LA.norm(query_vectorizer_array)*LA.norm(doc_vectorizer_array,axis=1)
    # sim = num/denom

    # num2 = ants_vectorizer_array.dot(doc_vectorizer_array.T)
    # denom2 = LA.norm(ants_vectorizer_array)*LA.norm(doc_vectorizer_array,axis=1)
    # sim2 = num2/denom2

    # final_sim = sum(sim_syn) - sum(sim_ant)
    final_sim = np.array(sim) - np.array(sim2)
    
    sims_idx = [(i, sim) for i, sim in enumerate(final_sim)]
    ranked = sorted(sims_idx, key=lambda x: x[1], reverse=True) 
    keys = list(tokens_map[city][category].keys())

    ranked_translated = [(keys[x[0]], x[1]) for x in ranked]

    return ranked_translated


def get_matchings_cos_sim(city, category, query):
    with open('app/irsystem/models/tokens_mapping.json') as f:
        tokens_map = json.load(f)

    # with open('app/irsystem/models/stemmed_mapping.json') as f:
    #     tokens_map = json.load(f)
    with open('app/irsystem/models/ranking_mapping.json') as f:
        rankings_map = json.load(f)
    if not query:
        return sorted(tokens_map[city][category].items(), key=lambda x: x[1], reverse=True)

    query_antonyms, query_synonyms = get_query_antonyms(query)

    # synonyms_forms = many_word_forms(query_synonyms)
    # antonyms_forms = many_word_forms(query_antonyms)

    synonyms_forms = query_synonyms
    antonyms_forms = query_antonyms

    # list of all review strings (each place has a single review string of all reviews) with
    # the query string as the last vector
    to_vectorize = [tokens_map[city][category][x] for x in tokens_map[city][category]]  + [antonyms_forms] + [synonyms_forms]
    # tfidf_vec = build_vectorizer()
    tfidf_mat = tfidf_vec.fit_transform(to_vectorize).toarray()

    vocab = tfidf_vec.get_feature_names()


    # calculate cosine sims between each place's tf-idf vector and the query string vector
    cos_sims = [get_cos_sim(tfidf_mat[i], tfidf_mat[-1]) - get_cos_sim(tfidf_mat[i], tfidf_mat[-2]) for i in range(len(tfidf_mat)- 2)]
    sims_idx = [(i, sim) for i, sim in enumerate(cos_sims)]
    ranked = sorted(sims_idx, key=lambda x: x[1], reverse=True)  # slice off query

    # translate from id's to names
    keys = list(tokens_map[city][category].keys())

    ranked_translated = [(keys[x[0]], x[1]) for x in ranked]

    return ranked_translated


def LSI_SVD(query, courseVecDictionary, city, category, reverseIndexDictionary, svdDictionary):
    # courseVecDictionary[class selected]
    vec, docVectorizerArray = courseVecDictionary[city][category]
    reverse_index = reverseIndexDictionary[city][category]

    #query = utils.tokenize_SpaCy(query)
    queryVectorizerArray = np.zeros((docVectorizerArray.shape[1],))
    # feature_list = vec.get_feature_names()
    for w in query.split(" "):
        idx = reverse_index.get(w, -1)
        print(idx)
        if idx > 0:
            print("here2")
            queryVectorizerArray[idx] += 1.0
    queryVectorizerArray *= vec.idf_

    if queryVectorizerArray.sum() == 0:
        return []
    print(svdDictionary[city][category])
    # u,s,v_t = np.linalg.svd(docVectorizerArray.T) #svd on tfidf documents
    u, s, v_t = svdDictionary[city][category]
    #get query vector svd
    k = int(0.6 * v_t.shape[0])  # 500
    q = queryVectorizerArray # q =
    q_hat = np.matmul(np.transpose(u[:, :k]), q)

    sim = []
    for i in range(docVectorizerArray.shape[0]): #rows for each thing calculating
        # app.logger.debug("Shape of s: {}".format(np.diag(s[:k]).shape))
        # app.logger.debug("Shape of v_t: {}".format(v_t[:k,i].shape))
        # app.logger.debug("Shape of q_hat: {}".format(np.transpose(q_hat).shape))
        num = np.matmul(np.matmul(np.diag(s[:k]), v_t[:k, i]), np.transpose(q_hat)) #dot product of svd_dict at i dot product of svd_query
        denom = np.linalg.norm(np.matmul(np.diag(s[:k]), v_t[:k, i])) * np.linalg.norm(q_hat)
        sim.append(num / denom)

    return np.array(sim)


def within_rad(city, top_hotels, top_rests, top_attract, radius):  # top_attract,
    
    if city == '':
        return {}
    with open('app/irsystem/models/inverted-index.json') as f:
        inv_ind = json.load(f)
        f.close()
    with open('app/irsystem/models/distance-matrices.json') as f:
        distances = json.load(f)
        f.close()
    with open('app/irsystem/models/all_info.json') as f:
        info = json.load(f)[city]
        f.close()
    with open('app/irsystem/models/ranking_mapping.json') as f:
        rankings_map = json.load(f)[city]
        f.close()
    with jsonlines.open(f'app/irsystem/models/sites/{city}-restaurant-sites.jsonl') as reader:
        for obj in reader:
            rest_sites= obj
    with jsonlines.open(f'app/irsystem/models/sites/{city}-accommodation-sites.jsonl') as reader:
        for obj in reader:
            acc_sites= obj
    with jsonlines.open(f'app/irsystem/models/sites/{city}-attraction-sites.jsonl') as reader:
        for obj in reader:
            att_sites= obj


    within_rad = {}
    h_count = 0
    for h in top_hotels:
        if h_count >= 10:
            break
        restaurants = []
        rest_count = 0
        for r in top_rests:
            if rest_count >= 10:
                break
            #dist = distances[city][order[1]][inv_ind[city][order[1]][r]][inv_ind[city][order[0]][h]]
            dist = distances[city]['restaurant'][inv_ind[city]['restaurant'][r]][inv_ind[city]['accommodation'][h]]
            if dist <= radius:
                rest_info = info['restaurant'][r]   
                rest_dict = {"name": r.title(), "distance": round(dist), "address": rest_info["address"], "reviews": [], "subcategory": "", "url": rest_sites[r], "target": "_blank"}
                if rest_dict["url"] == "":
                    rest_dict["url"] = "#"
                    rest_dict["target"] = "_self"
                if "reviews" in rest_info:
                    rest_dict["reviews"] = rest_info["reviews"][:5]
                if "subCategory" in rest_info:
                    rest_dict["subcategory"] = rest_info["subCategory"]
                rest_dict["rating"] = rankings_map['restaurant'][r] if rankings_map['restaurant'][r] > 0 else "N/A"
                restaurants.append(rest_dict)
                rest_count += 1
        attractions = []
        att_count = 0
        for a in top_attract:
            if att_count >= 10:
                break
            #dist = distances[city][order[2]][inv_ind[city][order[2]][a]][inv_ind[city][order[0]][h]]
            dist = distances[city]['attraction'][inv_ind[city]['attraction'][a]][inv_ind[city]['accommodation'][h]]
            if dist <= radius:
                attr_info = info['attraction'][a]   
                attr_dict = {"name": a.title(), "distance": round(dist), "address": attr_info["address"], "reviews": [], "subcategory": "", "url": att_sites[a], "target": "_blank"}
                if attr_dict["url"] == "":
                    attr_dict["url"] = "#"
                    attr_dict["target"] = "_self"
                if "reviews" in attr_info:
                    attr_dict["reviews"] = attr_info["reviews"][:5]
                if "subCategory" in attr_info:
                    attr_dict["subcategory"] = attr_info["subCategory"]
                attr_dict["rating"] = rankings_map['attraction'][a] if rankings_map['attraction'][a] > 0 else "N/A"
                attractions.append(attr_dict)
                att_count += 1
        acc_info = info['accommodation'][h]   
        acc_dict = {"name": h.title(), "address": acc_info["address"], "reviews": [], "subcategory": "", "url": acc_sites[h], "target": "_blank"}
        if "reviews" in acc_info:
            acc_dict["reviews"] = acc_info["reviews"][:5]
        if "subCategory" in acc_info:
            acc_dict["subcategory"] = acc_info["subCategory"]
        acc_dict["rating"] = rankings_map['accommodation'][h] if rankings_map['accommodation'][h] > 0 else "N/A"
        if not acc_dict["url"]:
            acc_dict["target"] = "_self"
            acc_dict["url"] = "#"
        within_rad[h] = {'restaurants': restaurants, 'attractions': attractions, 'accommodation': acc_dict}
        h_count += 1

    return within_rad

