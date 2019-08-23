---
layout: default
title: Classification Functions
code_title: Classification_functions.py
---
# Core functions

In the following there are three functions, two used for the classification of tweets in "TweetClassification.py" and one used to adjust class names, since at the moment at which the code was developed the final version of the data-set with different tags collapsed together was not ready.

## Adjust class names
The ```class_adjust``` function takes as parameter the tag of the tweet and it applies the following rules:

| Tag                                                         | Class          |
|-------------------------------------------------------------|----------------|
| SportsOrganization,SportsTeam                               | Sports         |
| MusicAlbum,MusicGroup,MusicRecording                        | Music          |
| Book,BookSeries                                             | Book           |
| EducationalOrganization,Organization,GovernmentOrganization | Organization   |
| Movie,MovieSeries                                           | Movie          |
| VideoGame,VideoGameSeries                                   | VideoGame      |
| Other                                                       | Leave as it is |


In this way we reduce the amount of classes. The function is very simple, it has different lists (one for each "collapsed-class") and we do the check: if the input ```tag``` is in one of the list, we assign the correct class.

```python
def class_adjust(tag):
    sports = ["SportsOrganization","SportsTeam"]
    music = ["MusicAlbum","MusicGroup","MusicRecording"]
    organization = ["EducationalOrganization","Organization","GovernmentOrganization"]
    book = ["Book","BookSeries"]
    movie = ["Movie","MovieSeries"]
    video = ["VideoGame","VideoGameSeries"]

    if tag in sports:
        c = "Sports"
        return c

    if tag in music:
        c = "Music"
        return c

    if tag in organization:
        c = "Organization"
        return c

    if tag in book:
        c = "Book"
        return c

    if tag in movie:
        c = "Movie"
        return c

    if tag in video:
        c = "VideoGame"
        return c

  
    return tag
```

## Classification functions
In doing the classification, after the pre-processing, we look for common nodes in the lineages of the mentions extracted from the tweet. The difference among the classification functions depends on the number of nodes that different lineages (list of node of one entity)
may have in common, there can be:
- one one node in common,
- more than one node in common (best case),
- no node in common (worst case).

As a consequence there are three different types of classification function and in each of them we tried to select the best type possible by relaying on two different aspects: the score of one particular node and the probability that a certain tweet's author talks about a certain topic. The pre-existing scores of the
nodes are taken by the knowledge base used (Google Knowledge Graph), then they are updated and incremented thanks to the probabilities computed on the classified data.

## Parameters

All the three function take as input the following parameters:

1. **common_nodes.** Is a list of the common nodes found by scanning the lineages of the entities of that particular tweet.
2. **target_names.** Is the name of the classes of our classification problem.
3. **author.** Tweet's author.
4. **p.** The probabilities dictionary, where for each author there is a list of topic-probability value pair, depending how much frequent a certain author tweets about a certain topic:

```python
     {
    '1RealJoeyB': [('Event', 0.5), ('Music', 0.5)], 
    '1Tyvis': [('Movie', 1.0)], 
    
    }
```
### Each classification function has one single 

- [```one_nodes_types(entities,inverted_index,target_names,author,p)``` ](/pages/one.html)
- [```multiple_nodes_types(entities,inverted_index,target_names,author,p)``` ](/pages/multiple.html)
- [```no_common_nodes_types(entities,inverted_index,target_names,author,p)``` ](/pages/none.html)
    
