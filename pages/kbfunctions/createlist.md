---
layout: function
title: createListOfNodes
code_title: KBfunctions.py - createListOfNodes
main: /wir_project/pages/kb
---
# This is an important function!
## It allows us to navigate better between the nodes

This function put the nodes in a list, where each element of the list is a dictionary with the following fields:
- ***id***: the node id;
- ***name***: the node name;
- ***types***: the list of the types of the node;
- ***score***: the score of the node.

In the search function we decided to put a limit for the number of returned nodes, ***in particular we will have at most 50 nodes***. 

### This choice was due to the fact that in the GKG no all the entity have enough nodes, indeed for some entitiy there is no node at all! In this particular case, sometimes the API returns an error, this is why we decided for this limit.

```python
def createListOfNodes(query):
    nodes = search(query)
    listOfNodes = list()
    if 'itemListElement' not in nodes:
        return listOfNodes

    for element in nodes['itemListElement']:
        id = ""
        name = ""
        score = 0.00
        types = list()

        if '@id' in element['result']:
            id = element['result']['@id']

        if 'name' in element['result']:
            name = element['result']['name']

        if '@type' in element['result']:
            types = element['result']['@type']

        if 'resultScore' in element:
            score = element['resultScore']

        toInsert = {
            'id': id,
            'name': name,
            'types': types,
            'score': score
        }
        listOfNodes.append(toInsert)

    return listOfNodes
```
The output of the function is a list of ```dict``` elements.
