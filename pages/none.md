---
layout: default
title: Classification Functions
code_title: Classification_functions.py - no_common_node_types
---
# The common nodes list is empty
We initialize three variables:
- ***first_nodes***. Is a list that will contain the nodes extracted from the lineages of entities of the tweet.
- ***all_types***. Is a list that will contain the types extracted as in the two previous functions ```one_node_types``` and  ```multiple_node_types```.
- ***not_in***. Is a boolean variable use to extract the types as in the two previous functions ```one_node_types``` and  ```multiple_node_types```.

```python
    first_nodes = list()
    all_types = list()
    not_in = False
```
## Our strategy
Since we do not have any node in common, whenever is possible for each entity we retrieve all the nodes from the index, searching for the best type by considering also the author and the associated probabilities.

For each entity in the tweet that we have extract we get the nodes from the index.
```python
    for e in entities:
        nodes = inverted_index.get(e)
        if nodes:
            # the nodes are sorted according to the score, from the highest to the lowest.
            nodes = sorted(inverted_index.get(e), key=lambda i: i["score"],reverse=True)
```
At the beginning we pick only the first node, but...

```python
            n1 = nodes[0]
            first_nodes.append(n1)
```
...if we have more than one nodes, we take all the node of the lineage of that particular entity in order to have more types to extract.

```python
            if len(nodes) > 1:
                for n in nodes:
                    first_nodes.append(n)
```
We may have three different cases according to the lenght of the ```first_nodes``` list.

## More than one node
### This happen if the tweet has more than one entity with multiple nodes in its lineage

If we have more than one node in ```first_nodes``` we applicate the same principle of ***multiple node*** case. For each node in the list we extract the types, storing them in a and if "Thing" is present we remove it. For each type of that node we:
- we search for the type t in the ```all_types``` list,
- if the type is not present we have to add it in this way:
	- ```to_insert = {"type": t, "count": 1, "score": elem[2]}```
	where:
		- ***type*** is assigned to the current type name ***t***;
		- ***count*** is assigned to one, since is the first time we meet that type,
		- ***score*** is the score of that type, given in that node.
		
As usual at the beginning we remove the "Thing" type.

***The only difference here is that we are operating with nodes coming from different lineages.*** Let's examine the case in which the type is not present in the ```all_types``` list:

```python
    if len(first_nodes) > 1:

        # for each node
        for elem in first_nodes:
            # we extract the types and we remove "Thing" if it is present.
            types = list(elem.get("types"))
            print(types)
            if "Thing" in types:
                types.remove("Thing")

            # for each type we repeat the reasoning done in the case of multiple nodes
            for t in types:
                # we search for the type t in the "all_types" list.
                # if the type is not present in "all_types" we have to add it.

                there = next((item for item in all_types if item["type"] == t), False)
                if not there:
                    to_insert = {"type": t, "count": 1, "score": elem.get('score')}
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
                        print(t, to_change["score"])
```
In the case the type is contained in the data-structure containing the probabilities we increment the score by considering the probabilities, so the overall score will be higher. The only thing that changes here wrt the previous cases, is how the score is retrieved from the element since ```fist_nodes```
 stores the nodes of the index that are dictionaries, this is why we have the "get" method.
```python
                        to_change["score"] = to_change["score"] + (elem.get('score')*(1 + (couple[1]*1000)))
                        print(t, to_change["score"])

                    else:
                        to_change = all_types[all_types.index(there)]
                        to_change["count"] = to_change["count"] + 1
                        print(t, to_change["score"])

```
If the type is not among the ones used by the author of the current tweet we update the score just by adding the score of the current node in the ```fist_nodes``` list.
```python
                        
                        to_change["score"] = to_change["score"] + elem.get('score')
                        print(t, to_change["score"])

        all_types = sorted(all_types, key=lambda i:  i['score'], reverse=True)

        print(all_types)
        select_type = all_types
        predicted_tag = ""
```
Same check for the types of the case of multiple nodes...

```python
        while predicted_tag not in target_names:
            print(predicted_tag)
            if not select_type:
                not_in = True
                break

            predicted_tag = class_adjust(select_type[0].get('type'))
            select_type.pop(0)
```
***What change is how we beahave in the case there is no matching with our selected classes***. Since in the case we of no common nodes there are the majority of errors, we decide to "help" the classifier by "cheating" a little bit by selecting as ```predicted_tag``` the type with the highest probability of author of the tweet.

```python
        if not_in:
            predicted_tag = max(p.get(author), key=lambda item: item[1])[0]

        # print("Sorted: " + str(all_types))

        return predicted_tag
```
## Only one node
### This happen if the tweet has only one entity with one-node-lineage (yeah, it seems strange but could happen).

We just take the only node that we have.

```python 
    elif len(first_nodes) == 1:
        types = list(first_nodes[0].get("types"))
        score = first_nodes[0].get("score")
        print(types)

        # we remove "Thing" if present
        if "Thing" in types:
            types.remove("Thing")

```
For all types that are present in this node, we barely do the same of what we have done in multiple node case, with the difference that we do not update the scores (since we are in the case of only one node), so in order to get higher scores among the types we use the probabilities values.
```python
        for t in types:
            present = next((item for item in p.get(author) if item[0] == t), False)
            if present:
                couple = next(item for item in p.get(author) if item[0] == t)
                to_insert = {"type": t, "count": 1, "score": score * (1 + (couple[1] * 1000))}
                all_types.append(to_insert)
            else:
                to_insert = {"type": t, "count": 1, "score": score}
                all_types.append(to_insert)

        all_types = sorted(all_types, key=lambda i: i['score'], reverse=True)
        print(all_types)
        select_type = all_types
        predicted_tag = ""
```
Same stuff as in the case of multiple nodes in common...

```python
        while predicted_tag not in target_names:
            print(predicted_tag)
            if not select_type:
                not_in = True
                break

            predicted_tag = class_adjust(select_type[0].get('type'))
            select_type.pop(0)

        if not_in:
            # predicted_tag = all_types[0].get('type')
            # predicted_tag = "Thing"
            predicted_tag = max(p.get(author), key=lambda item: item[1])[0]

        return predicted_tag
```
## Only one node
### Maybe was not possible to extract any entity from the tweet or the entities have empty lineages:(

If the we are in the case in which the entities have empty lineages, we return the type with highest probabilityfor the author. This really helps the classifier and this choice is due the fact that in the case in which have no nodes in common is difficult to establish which is the correct class and so is the part where the number of error increases.
```python
    else:
        #predicted_tag = "Thing"
        predicted_tag = max(p.get(author), key=lambda item: item[1])[0]
        return predicted_tag

```
### Links

- [```one_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/one.html)
- [```multiple_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/multiple.html)
- [```no_common_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/none.html)
    
