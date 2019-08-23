---
layout: function
title: tweetTag
code_title: KBfunctions.py - tweetTag
main: /wir_project/pages/kb
---
# Common or not common?
## This functions returns the possible type for a particular tweet in the case there are common nodes or not.
The function takes as input the results that are the list (possibly empty) of common nodes retured from the ```commonNodes``` function and the list of the nodes for each entity in that tweet.

This function returns the set of tags that better describes the tweet, considering the two cases:

1. There ***are common nodes*** of the lineages of the mentions.
2. There are ***not common nodes***.

In the first case we consider all the types of the common nodes once and we return them, avoiding the "Thing"-type.
In the second case we just pick the first node of the lineage, with higher score and we return the types of that node.
```python
def tweetTag(results,listOfEntites):
#I have two possible cases:
    #result is not empty
    if len(results) != 0:
        tags = set()
        for elem in results:
            for tag in elem.get('types'):
                tags.add(tag)

        tags.remove("Thing")
        return tags

    #result is empty so there are no nodes in common
    else:
        tags = set()
        for list in listOfEntites:
            if list:
                for tag in list[0].get('types'):
                    tags.add(tag)

        tags.remove("Thing")
        return tags

```