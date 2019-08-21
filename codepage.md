#classificationfunctions
```
from KBfunctions import *
from KaiCode_preprocessing import *
import itertools
import json
```

In the following there are three functions, used for the classification of tweets ("TweetClassification.py") and one
used to adjust class names.

CLASSIFICATION FUNCTIONS:
-------------------------
The difference among the functions depends on the number of nodes that different lineages (list of node of one entity)
have in common, there can be:

- one node in common,
- more than one node in common (best case),
- no node in common (worst case).

In each function we tried to select the best type possible by relaying on two different aspects: the score of one 
particular node and the probability that a certain tweet author talks about a certain topic; the different scores of the
node are given by the knowledge base used (Google Knowledge Graph) and the probabilities were computed once we get the
classified dataset.


ADJUST CLASS NAMES:
-------------------
Once we had our dataset labeled with one single representative tag for each tweet, there was the problem that some tag
can be "collapsed" into one class, in particular:

- (SportsOrganization,SportsTeam)        ------->    Sports
- (MusicAlbum,MusicGroup,MusicRecording) ------->    Music
- (VideoGame,VideoGameSeries)            ------->    VideoGame
-  ...

In this way we reduced the number of classes and then an extra field containing the class was added to the dataset.


THE ENTITIES IN THE TWEET HAVE ONLY ONE NODE IN COMMON.
------------------------------------------------------
The parameters for the function are:

--> common nodes:...the list of common nodes;

--> target_names:...the list of the classes in our dataset; 

--> author:.........the author of the tweet;

--> p:..............the data-structure containing the probabilities, in particular it is a dict having as key the 
                    author names.
```
def one_node_types(common_nodes,target_names,author,p):
    """
    @param common_nodes:
    @param target_names:
    @param author:
    @param p:
    @return:
    """
    # if the list containing the common nodes has lenght equal to 1, we have to
    # extract the only node in, it will be our representative node.
    representative_node = common_nodes[0]
    types = list(representative_node[1])
    not_in = False
    print(types)

    author_types = p.get(author)
    max_type = max(author_types, key=lambda item: item[1])
    possible_type = max_type[0]

    if possible_type in types:
        print("The possible type is " + possible_type)
        return possible_type
    # we can have one or more types in the list of this single node.
    if len(types) > 1:
        # if we have more than one type we can safelly remove the "Thing" type
        # that it is not so informative.
        types.remove("Thing")
        select_type = types
        predicted_tag = ""

        # while the predicted tag is not one of the classes of our data
        # we keep searching through the types of the node
        while predicted_tag not in target_names:
            print(predicted_tag)

            # if the list of types we exit from the while-loop
            if not select_type:
                not_in = True
                break
            predicted_tag = class_adjust(select_type[0])
            select_type.pop(0)

        if not_in:
            # in the case we have scanned all types we select the "Thing" as class for the tweet
            predicted_tag = "Thing"

        return predicted_tag

    # if we have only one type, we have to select it in the case is acceptable.
    else:
        if types[0] in target_names:
            predicted_tag = types[0]

        # otherwise we have to choose for "Thing", as in the case above.
        else:
            predicted_tag = "Thing"

    return predicted_tag

```

