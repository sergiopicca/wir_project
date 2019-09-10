---
layout: default
title: Classification Functions
code_title: Classification_functions.py - one_node_types
---
# The entities have only one node in common

If the list containing the common nodes has lenght equal to 1, we have to extract the only node in, it will be our representative node.
```python
    representative_node = common_nodes[0]
    types = list(representative_node[1])
    not_in = False
    print(types)
```
Then we extract the types of tweets written by the current author, in particular the types are not strings, since they are extracted from ```p```, they are tuples ```(type t, probability_of_t)```. We sort them in decreasing order. If the type with the highest probability is one among the types contained in the representative node we return it.

```python
    author_types = p.get(author)
    max_type = max(author_types, key=lambda item: item[1])
    possible_type = max_type[0]

    if possible_type in types:
        print("The possible type is " + possible_type)
        return possible_type
```

We can have one or more types in the list of this single node.
```python
    if len(types) > 1:
```
If we have more than one type we can safelly remove the "Thing" type that it is not so informative.
```python
        types.remove("Thing")
        select_type = types
        predicted_tag = ""
```
While the predicted tag is not one of the classes of our data we keep searching through the types of the node. We make this check since in the ***Google Knowledge Graph there a huge variety of types***, so we needed to do a simplification, otherwise the number of classes would grow very fast!

```python
        while predicted_tag not in target_names:
            print(predicted_tag)

            # if the list of types we exit from the while-loop
            if not select_type:
                not_in = True
                break
            predicted_tag = class_adjust(select_type[0])
            select_type.pop(0)
```
If we don't have a match with our set of classes we decide for the most general class "Thing".

```python
        if not_in:
            # in the case we have scanned all types we select the "Thing" as class for the tweet
            predicted_tag = "Thing"

        return predicted_tag

```
If we have only one type, we have to select it in the case is acceptable, otherwise "Thing" again.

```python
    else:
        if types[0] in target_names:
            predicted_tag = types[0]

        # otherwise we have to choose for "Thing", as in the case above.
        else:
            predicted_tag = "Thing"

    return predicted_tag
```

### Links

- [```one_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/one.html)
- [```multiple_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/multiple.html)
- [```no_common_nodes_types(entities,inverted_index,target_names,author,p)``` ](/wir_project/pages/none.html)