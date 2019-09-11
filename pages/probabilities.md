---
layout: default
title: Probabilities
code_title: AuthorAndClasses.py
---

This function computes the probabilities by reading the tweets and checking how many tweets were written by a particular
author, looking for the types and their occurrencies, once these values are computed we store the probabilities p, in a 
dictionary indexed by the author's name, where p is:

```python
                        
                      #tweets_of_a_with_type_t 
for author a, t, p =  ________________________

                        #tweets_of_a
```
# Get probabilities

```python
def get_probabilities():
    dataset_paths = ["CSV/Sergio_one_label_data.csv","CSV/Gianluca_one_label_data.csv","CSV/Kai_one_label_data.csv"]
    tweet_list = list()

    for path in dataset_paths:
        lst = readSingleLabeledCSV(path)
        tweet_list = tweet_list + lst

    authors = list()
    probabilities = dict()

    for t in tweet_list:
        a = t.get('screen_name')
        c = class_adjust(t.get('single_tag'))
        there = next((item for item in authors if item["author"] == a), False)
```
first each author is stored in a list of dictionary called "authors"
in order to count how many tweet were written by a particular author a,
with the indication of the class and its occurencies.

```python
 if not there:
            classes = list()
            classes.append((c,1))
            to_insert = {"author": a, "classes": classes,  "count": 1}
            authors.append(to_insert)

        else:
            to_change = authors[authors.index(there)]
            to_change["count"] += 1
            to_update = next((item for item in to_change.get("classes") if item[0] == c),False)

            if not to_update:
               to_change.get("classes").append((c,1))

            else:
                elem = to_change.get("classes")[to_change.get("classes").index(to_update)]
                to_change.get("classes").remove(elem)

                to_add = (elem[0],elem[1]+1)
                to_change.get("classes").append(to_add)
```
"authors" list is sorted by author names

```python
authors = sorted(authors, key=lambda i: i["author"], reverse=False)
```
here we create the dictionary indexed by the author's name
```python
    for elem in authors:
        a = elem.get("author")
        classes = elem.get("classes")
        d = elem.get("count")
        sequence = list()

        for c in classes:
            prob = c[1]/d
            sequence.append((c[0],prob))

        probabilities[a] = sequence

    return probabilities
```


