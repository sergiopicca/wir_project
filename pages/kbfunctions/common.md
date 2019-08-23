---
layout: function
title: commonNodes
code_title: KBfunctions.py - common
main: /wir_project/pages/kb
---
# Where the main intuition takes place
## Actually this function was used to just try the intuition explained in the [Homepage](/index.html) in some experiment

This function returns a list containing common nodes of two different lineages l1 and l2, represented by two lists; then the new score is computed and it is obtained by adding the two score, s1 + s2. The 
formula on the paper does not apply since the scores are not percentage.

The function takes as parameter:
- two ```sets```, containing the id of the nodes of two lineages. The choice was due the fact that we wanted a fast way to compute intersection.
- two ```lists```, containg the nodes of the same two lineages with all information (types, scores, ...).

```python
def commonNodes(set_one, set_two, list_one, list_two):
    results = list()

    for elem in list_one:
        if elem.get('id') in set_one.intersection(set_two):
            id = elem.get('id')
            name = elem.get('name')
            types = elem.get('types')
            s1 = elem.get('score')

            for item in list_two:
                if item.get('id') in set_one.intersection(set_two) and item.get('id') == id:
                    s2 = item.get('score')
                    score = s1 + s2
                    toInsert = {
                        'id': id,
                        'name': name,
                        'types': types,
                        'score': score
                    }
                    results.append(toInsert)

    return results
```
This function returns a list containing common nodes of two different lineages l1 and l2, represented by two lists; then the new score is computed and it is obtained by adding the two score, s1 + s2. The 
formula on the paper does not apply since the scores are not percentage.
