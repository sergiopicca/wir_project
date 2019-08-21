# Classification functions
```
from KBfunctions import *
from KaiCode_preprocessing import *
import itertools
import json
```

In the following there are three functions, used for the classification of tweets ("TweetClassification.py") and one
used to adjust class names.

## CLASSIFICATION FUNCTIONS:

The difference among the functions depends on the number of nodes that different lineages (list of node of one entity)
have in common, there can be:
- one node in common,
- more than one node in common (best case),
- no node in common (worst case).

In each function we tried to select the best type possible by relaying on two different aspects: the score of one 
particular node and the probability that a certain tweet author talks about a certain topic; the different scores of the
node are given by the knowledge base used (Google Knowledge Graph) and the probabilities were computed once we get the
classified dataset.

## ADJUST CLASS NAMES:

Once we had our dataset labeled with one single representative tag for each tweet, there was the problem that some tag
can be "collapsed" into one class, in particular:

