import pickle
import jsonlines
import json
import numpy.linalg as LA

import numpy as np
import word_forms
from word_forms.word_forms import get_word_forms

with open("app/irsystem/models/synonyms.json") as f:
    syn_dict = json.load(f)
    f.close()

with open("app/irsystem/models/antonyms.json") as f:
    ant_dict = json.load(f)
    f.close()

def get_query_antonyms(query):
    antonyms = []
    synonyms = []
    for q in query.split(" "):
        syn = syn_dict.get(q)
        ant = ant_dict.get(q)
        if not syn:
            synonyms += [q]
        else:
            synonyms += syn[:10] + [q]
        if ant:
            antonyms += ant[:10]

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

    # synonyms_forms = query_synonyms.split(" ")
    # antonyms_forms = query_antonyms.split(" ")

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
    k = int(0.6 * v_t.shape[0])
    q = query_vectorizer_array
    q_hat = np.matmul(np.transpose(u[:,:k]),q)
    q_2 = ants_vectorizer_array
    q_hat_2 = np.matmul(np.transpose(u[:, :k]), q_2)
    sim = []
    sim2 = []
    for i in range(doc_vectorizer_array.shape[0]):
        num = np.matmul(np.matmul(np.diag(s[:k]),v_t[:k,i]),np.transpose(q_hat))
        denom = np.linalg.norm(np.matmul(np.diag(s[:k]),v_t[:k,i]))*np.linalg.norm(q_hat)
        sim.append(num/denom)
        num = np.matmul(np.matmul(np.diag(s[:k]), v_t[:k, i]), np.transpose(q_hat_2))
        denom = np.linalg.norm(np.matmul(np.diag(s[:k]), v_t[:k, i])) * np.linalg.norm(q_hat_2)
        sim2.append(num / denom)

    final_sim = np.array(sim) - np.array(sim2)
    
    sims_idx = [(i, sim) for i, sim in enumerate(final_sim)]
    ranked = sorted(sims_idx, key=lambda x: x[1], reverse=True) 
    keys = list(tokens_map[city][category].keys())

    ranked_translated = [(keys[x[0]], x[1]) for x in ranked]

    return ranked_translated

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

