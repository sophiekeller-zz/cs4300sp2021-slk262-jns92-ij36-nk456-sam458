import csv
import json

data = {}
with open("synonyms.csv", encoding='utf-8') as csvf:
  csvReader = csv.DictReader(csvf)
    
  # Convert each row into a dictionary
  # and add it to data
  for rows in csvReader:
      # Assuming a column named 'No' to
      # be the primary key
      key = rows['lemma']
      all_words = []
      if key == "custom":
        print(rows["synonyms"])
      for word in rows["synonyms"].split(";"):
        all_words += word.split("|")
      if key in data:
        data[key] += all_words
      else:
        data[key] = all_words

with open("synonyms.json", "w") as f:
  json.dump(data, f)