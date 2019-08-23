---
layout: default
title: Creating the inverted index
code_title: InvertedIndex.py
---
# We want an inverted index

## Using everytime the API is not good

If we try to classify the tweets by asking everytime to the API, we will have many errors, because it does not handle frequent calls (obviously we did not pay to use it, we used the ***free version***). We decided to store the entities of each tweet of our collection in an inverted index, where we have the couple ```(entity, list of nodes)```.

```python
dataset_paths = ["CSV/Sergio_one_label_data.csv","CSV/Gianluca_one_label_data.csv","CSV/Kai_one_label_data.csv"]
tweet_list = list()
lst = list()
set_of_entities = set()
pseudo_inverted_index = dict()
```
# Read the tweets
We first read the tweets, the ones previously labeled with multiple tags, then we append them to the ```tweet_list```. Then the second thing to do is to extract the entities for each tweet to store them in a file called the ```entity_file.txt```. ***We need to store them in order to be more efficient, write the index one entity at the time will be too slow.***

```python
for path in dataset_paths:
    lst = readSingleLabeledCSV(path)
    tweet_list = tweet_list + lst

if not os.path.isfile("TXT/entity_file.txt"):
    for t in tweet_list:
        text = t.get('full_text')
        entities = preprocessing(text)
        entity_file = open("TXT/entity_file.txt", 'a')
        for e in entities:
            entity_file.write(e + "\n")

        entity_file.close()
```
# The "error" variable
### In this code we do many call to GKG API, so sometimes an error will raise: 503 Service Unavailable error.

Many call to the API will raise the 503 Service Unavailable error, so the code will stop and we should run it again manually. In order to avoid this ***boring thing*** we handle the error by using a ```try: ... except urllib.error.HTTPError as err:``` statement later in the code triggered in the case of 503 error. We use a variable called ```error``` setted to ```True```, then in the loop cycle is immediately switched to ```False```, it will return ```True``` only in the case we catch and error. 

```python
#This variable is for error handling, in the case the API does not work (503 error: service not avaible)
error = True
while(error):
    print("A new iteration begin (there was an error)...\n")
    time.sleep(5)

    #this is the file in which all the entities are stored
    #the usage of a file is requested to speed up the process
    entity_file = open("TXT/entity_file.txt", 'r')
    print("Reading entities...\n")
    all_entities = entity_file.readlines()

    #words for which the search in GKG does not work
    stopwords = ['Part','Man','Good','Back','YouTube','LIVE','House','People','Album','Way','Love','How','Life']
    for e in all_entities:
        formatted_line = e.replace('\n', '')
        if formatted_line not in stopwords:
            set_of_entities.add(formatted_line)
    entity_file.close()
```
### In the above code there is the stopwords list, that contains entities that API couldn't get along with.

The strange thing is that if we use the GKG from the Google site with stopwords entities, it works! So we added manually the nodes associated to each of these entity manually...

### Suppose that we have written at most all the entities but at the end there is an error. What we do?!

According to what we have said there is no escape, we have to start all the process again. This is not true, since we used an ```already_written``` list, that contains the entities that have been already written in the index, so we do not need to start everything from scratch.

```python
    already_written = set()
    #the error variable is putted to false, hopefully it will not change
    error = False
```
If the file is present in the directory called ```JSON_index``` we retrieve the lines written.
```python
    if os.path.isfile('JSON_index/new_inverted_index.json'):
        with open('JSON_index/new_inverted_index.json', 'r') as f:
            lines = f.readlines()
            f.close()

        #this file will contain all the entities that are already written in the inverted index
        formattedFile = open("JSON_index/already_written.json", 'w')

        linesNumber = 0
```
We remove the last line because ***if an error occur the writing of the index simply stop and so the file could be ill-formed.*** Then we re-write the file well formed. 

### Is important to notice that the index file is not "pretty printed", otherwise we cannot retrieve each line as list of nodes. Indeed at the time the file is written an entity with its list of nodes represents a line.

```python
        print("Formatting the files...\n")
        #the last line is stripped out, because it may cause problem in reading the file
        print(len(lines[:-1]))
        for line in lines[:-1]:
            linesNumber = linesNumber + 1
            if linesNumber != len(lines[:-1]):
                formattedFile.write(line)
            else:
                line = line[:-2]
                formattedFile.write(line)

        formattedFile.write("\n}\n")
        formattedFile.close()

        #the 'already_written.json' once has been written is open to store in a set the entities already written
        with open('JSON_index/already_written.json', 'r') as f:
            data = json.load(f)
            for e in data.keys():
                already_written.add(e)
        f.close()
```
### We stress the concept a little bit
The index is re-written because it has to be well formed to add other entities. Let's suppose that the last line is: ```"entity_name": [{"id":``` in that case the row is incomplete, so it has to be removed so the file is overwritten.

```python
        with open('JSON_index/new_inverted_index.json', 'w') as f:
            for line in lines[:-1]:
                f.write(line)
        f.close()

    print("The entities are: " + str(len(set_of_entities)))
    print("The ALREADY WRITTEN entities are: " + str(len(already_written)))
    print("Start creating the inverted index...\n")
```
### we remove the entities already written

```python
    set_of_entities = set_of_entities - already_written
    print(set_of_entities)
    print("You still have to add: " + str(len(set_of_entities)) + "\n")
```
# Graffa variable
### We deal gain with the problem of ill-formness of the index file

Is the ```os.path.isfile('JSON_index/new_inverted_index.json')``` return ```True```, so it recognize the index as a ```.json``` file, the end parenthesis is present, so in order to add another entity we have to add it, because of the rules of a ```.json``` file.
```python
    graffa = False
    if os.path.isfile('JSON_index/new_inverted_index.json'):
        graffa = True

    with open('JSON_index/new_inverted_index.json', 'a') as fp:
        if not graffa:
            fp.write("{\n")

        whichOne = 0
        for e in set_of_entities:
            whichOne = whichOne + 1
            print(str(whichOne) + " - " + "Entity: " + e)
            #time.sleep(5)
            try:
                nodes = createListOfNodes(e)
            except urllib.error.HTTPError as err:
                if err.code == 503:
                    error = True
                    break
                else:
                    raise
            print("...")
            print("...")
```
### We sort the node, since we want to build an inverted index and by doing so the posting lists should be sorted.

```python
            #the entries in the posting list must be sorted!
            nodes = sorted(nodes, key=lambda i: i['id'])

            if whichOne != len(set_of_entities):
                #we add the entity and its nodes to the json file, if it is not the last a comma is required
                fp.write("\"" + e + "\": " + json.dumps(nodes) + ",\n")
            else:
                #otherwise the comma is not needed
                fp.write("\"" + e + "\": " + json.dumps(nodes) + "\n")

            print("Added to the index.\n")
            #time.sleep(10)
```
If no more error occurs, we add the last parenthesis.

```python
        if not error:
            fp.write("}")
```

