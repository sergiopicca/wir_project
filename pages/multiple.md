---
layout: default
title: Classification Functions
code_title: Classification_functions.py - no_common_node_types
---
We start by printing all the common nodes in the ```common_nodes``` list.
```python
print(common_nodes)
    all_types = list()
    not_in = False
```
For each node in the list we extract the types, storing them in a and if "Thing" is present we remove it. For each type of that node we:
- we search for the type t in the ```all_types``` list,
- if the type is not present we have to add it in this way:
	- ```to_insert = {"type": t, "count": 1, "score": elem[2]}```
	where:
		- ***type*** is assigned to the current type name ***t***;
		- ***count*** is assigned to one, since is the first time we meet that type,
		- ***score*** is the score of that type, given in that node.
		
As usual at the beginning we remove the "Thing" type.
```python
    for elem in common_nodes:
        types = list(elem[1])
        types.remove("Thing")

        for t in types:

            there = next((item for item in all_types if item["type"] == t), False)

            if not there:
                to_insert = {"type": t, "count": 1, "score": elem[2]}
                all_types.append(to_insert)
```
If the type is already present we increment its counter and upgraded its score. The update of the score is done differently depending on the type of the tweet if it is one of the type twitted by the author of the tweet or not.

```python
            else:
                present = next((item for item in p.get(author) if item[0] == t), False)
                if present:
                    couple = next(item for item in p.get(author) if item[0] == t)
                    print("Type " + t + " is present with prob. : " + str(couple[1]))
                    to_change = all_types[all_types.index(there)]
                    to_change["count"] = to_change["count"] + 1
                    print(t,to_change["score"])
```
In the case the type is contained in the data-structure containing the probabilities, we increment the score by considering the probabilities, so the overall score will be higher since this type is more likely to be the one of the tweet.

```python
                    to_change["score"] = to_change["score"] + (elem[2]*(1 + (couple[1]*1000)))
                    print(t,to_change["score"])
```
If the type is not among the ones used by the author of the current tweet we update the score just by adding the score of the current node in the ```common_nodes``` list.

```python                
                else:
                    to_change = all_types[all_types.index(there)]
                    to_change["count"] = to_change["count"] + 1
                    print(t, to_change["score"])

                    to_change["score"] = to_change["score"] + elem[2]
                    print(t, to_change["score"])

```
The ```all_types``` is sorted according to the score, in order to get the most likely type for the tweet on top. Them we do the same reasoning of the ```one_node_type``` function:
- if ```all_types``` is ***empty*** we select the "Thing" type for the tweet, since it is the most general one.
- in the case ```all_types``` ***is not empty*** we extract the types from the top of "all_types" since they are sorted in decreasing order of score, in that way we are sure to search first for the most probable type for the tweet, if the type is not in "target_names" list, we pop it out, and we look for the others.
- if we consume all the types and no one is among the selected classes, we again use "Thing".

```python
    all_types = sorted(all_types, key=lambda i: i['score'], reverse=True)

    print(all_types)
    predicted_tag = ""

    # if all_types is empty we choose for the "Thing" class.
    if not all_types:
        predicted_tag = "Thing"

    else:
        select_type = all_types
        predicted_tag = "\\"

        while predicted_tag not in target_names:
            print(predicted_tag)
            if not select_type:
                not_in = True
                break

            predicted_tag = class_adjust(select_type[0].get('type'))
            select_type.pop(0)

        if not_in:
            # predicted_tag = all_types[0].get('type')
            predicted_tag = "Thing"

    return predicted_tag


```
### Links

- [```one_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/one.html)
- [```multiple_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/multiple.html)
- [```no_common_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/none.html)