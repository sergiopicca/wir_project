---
layout: default
title: Tweet Classification
code_title: TweetClassification.py
---

# Here comes the magic
This is the actual code that makes the classification of tweets possible. 

## Read Tweets
We read the tweets from the different ```.csv``` files, we retrieve the index and store it in a variable, the variable ```classes``` is assigned with the name of a text-file containing the names of all the classes of our dataset.

```python
dataset_paths = ["CSV/Sergio_one_label_data.csv","CSV/Gianluca_one_label_data.csv","CSV/Kai_one_label_data.csv"]
inverted_index_path = "JSON_index/unpretty/inverted_index.json"
tweet_list = list()
classes = "classes.txt"
p = get_probabilities()

f = open(inverted_index_path,'r')
json_data = json.load(f)
f.close()

inverted_index = dict(json_data)
```
We read the tweets and we put them into a list. Then we have some different variables:
- ```stopwords = "Part"```. We are removing this entity because the KB presents an error.
- ```y_true```. A list of the classes of our dataset.
- ```y_pred = list()```. Class predicted by the usage of the KB


```python
for path in dataset_paths:
    lst = readSingleLabeledCSV(path)
    tweet_list = tweet_list + lst

stopwords = "Part"      # We are removing this entity because the KB presents an error
y_true = list()         # Tweets classified by ourselves
y_pred = list()         # Tweets classified by KB
count = 0               # We store how many times occurred a "Type"
```
```target_names``` will contain the names of the classes of the dataset, it is a list and we append to it each string in the ```classes.txt``` file (the filename is in the variable ```classes```), deleting the end of line characters.

```python
target_names = list()
less_tweet = tweet_list

f = open(classes,'r')
all_the_classes = f.readlines()
f.close()

for c in all_the_classes:
    if class_adjust(c.replace('\n','')) not in target_names:
        target_names.append(class_adjust(c.replace('\n','')))

print(target_names)
```
## Browse Tweets

```python

for tweet in less_tweet:
    print(tweet.get('id'))
```
We do preprocessing of the tweet by extracting entities.

```python
    entities = preprocessing(tweet.get('full_text'))
    author = tweet.get('screen_name')
```
We remove the "stopwords" from the entities. The "stopwords" variable is only equal to "Part" since
it is the only entity for the Google Knowledge Graph API returns an error, in particular
503: The service is currently unavailable. This happens every time we try to make a call to the API
by using "Part" as query, also in Google developer console.

```python
    if stopwords in entities:
        entities.remove(stopwords)
    print(entities)
    common_nodes = list()

    print("-" * 40)
    print("Author: " + author + " | " + str(p.get(author)))
    print("-" * 40)

    if entities:
        #print(entities)
        y_true.append(class_adjust(tweet.get('single_tag')))

```
We consider the different combination of entities extracted from the tweet and then we search them in to the index. Once we have found these entities we start looking both "posting lists" searching common nodes. The algorithm is the one saw for merging two posting lists, but in this case we use a list called ```common_nodes``` that will store the common nodes.

```python
        # this for-loop allow us to scan the "posting lists" aka the lineages of the inverted index we built.
        for x, y in itertools.combinations(entities, 2):
            lst1 = inverted_index.get(x)
            lst2 = inverted_index.get(y)
            k = 0
            j = 0
            if lst1 and lst2:
                while k != len(lst1) and j != len(lst2):
                    if lst1[k].get('id') == lst2[j].get('id'):

                        # if we find the common nodes between entities.For each common node, we
                        # will save the "id", the "types" and we will sum the "score" of the nodes,
                        # by sum the ones of both lineages.

                        common_nodes.append(
                            (lst1[k].get('id'),
                             lst1[k].get('types'),
                             lst1[k].get('score') + lst2[j].get('score')))
                        k = k + 1
                        j = j + 1
                    else:
                        if lst1[k].get('id') < lst2[j].get('id'):
                            k = k + 1
                        else:
                            j = j + 1
```
Depending on the size of the ```common_nodes``` list, we may have different cases, according to the length of common nodes. First of all:
- ```common_nodes``` is ***not empty***:
	- Only one node is present. [See the ```one_nodes_types``` ](/pages/one.html)
```python
        if common_nodes:
            print("\nCOMMON NODES!\n")
            common_nodes = sorted(common_nodes, key=lambda i: i[2])
            if len(common_nodes) == 1:
                print("One node in common...")
                predicted_tag = class_adjust(one_node_types(common_nodes,target_names,author,p))
                print("Predicted tag: " + str(predicted_tag) + " | True tag: " + str(class_adjust(tweet.get('single_tag'))))
                y_pred.append(predicted_tag)
                if predicted_tag != class_adjust(tweet.get('single_tag')):
                    one_node_error+=1
```
	- More node is present, in this case the lineages of the entities intersect in multiple nodes. [See the ```multiple_nodes_types``` ](/pages/multiple.html)
```python
            #if we have many nodes...
            else:
                print("More than one node in common...")
                predicted_tag = class_adjust(multiple_node_types(common_nodes,target_names,author,p))
                print("Predicted tag: " + str(predicted_tag) + " | True tag: " + str(class_adjust(tweet.get('single_tag'))))
                y_pred.append(predicted_tag)
                if predicted_tag != class_adjust(tweet.get('single_tag')):
                    more_node_error+=1
```

- ```common_nodes``` is ***empty***:
	- No common nodes between lineages. [See the ```no_common_nodes_types``` ](/pages/none.html)

```python
        else:
            print("No common nodes.")
            predicted_tag = class_adjust(no_common_nodes_types(entities, inverted_index, target_names,author,p))
            print("Predicted tag: " + str(predicted_tag) + "| True tag: " + str(class_adjust(tweet.get('single_tag'))))
            y_pred.append(predicted_tag)
            if predicted_tag != class_adjust(tweet.get('single_tag')):
                no_node_error += 1
                no_node.append((tweet.get('id'),predicted_tag,class_adjust(tweet.get('single_tag'))))

    print("-" * 40)
print(y_true)
print(y_pred)
```