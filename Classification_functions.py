from KBfunctions import *
from KaiCode_preprocessing import *
import itertools
import json

'''
In the following there are three functions, used for the classification of tweets ("TweetClassification.py") and one
used to adjust class names.

------------------------------------------------------------------------------------------------------------------------
CLASSIFICATION FUNCTIONS:
The difference among the functions depends on the number of nodes that different lineages (list of node of one entity)
have in common, there can be:

- one node in common,
- more than one node in common (best case),
- no node in common (worst case).

In each function we tried to select the best type possible by relaying on two different aspects: the score of one 
particular node and the probability that a certain tweet author talks about a certain topic; the different scores of the
node are given by the knowledge base used (Google Knowledge Graph) and the probabilities were computed once we get the
classified dataset.

------------------------------------------------------------------------------------------------------------------------
ADJUST CLASS NAMES:
Once we had our dataset labeled with one single representative tag for each tweet, there was the problem that some tag
can be "collapsed" into one class, in particular:

- (SportsOrganization,SportsTeam)        ------->    Sports
- (MusicAlbum,MusicGroup,MusicRecording) ------->    Music
- (VideoGame,VideoGameSeries)            ------->    VideoGame
-  ...

In this way we reduced the number of classes and then an extra field containing the class was added to the dataset.
'''

'''
THE ENTITIES IN THE TWEET HAVE ONLY ONE NODE IN COMMON.
------------------------------------------------------
The parameters for the function are:

--> common nodes:...the list of common nodes;

--> target_names:...the list of the classes in our dataset; 

--> author:.........the author of the tweet;

--> p:..............the data-structure containing the probabilities, in particular it is a dict having as key the 
                    author names.
'''
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


'''
THE ENTITIES IN THE TWEET HAVE MORE THAN ONE NODE IN COMMON.
------------------------------------------------------
The parameters for the function are:

--> common nodes:...the list of common nodes;

--> target_names:...the list of the classes in our dataset; 

--> author:.........the author of the tweet;

--> p:..............the data-structure containing the probabilities, in particular it is a dict having as key the 
                    author names.
'''
def multiple_node_types(common_nodes,target_names,author,p):
    """

    @param common_nodes:
    @param target_names:
    @param author:
    @param p:
    @return:
    """
    print(common_nodes)
    all_types = list()
    not_in = False

    for elem in common_nodes:
        types = list(elem[1])
        types.remove("Thing")

        for t in types:

            # we search for the type t in the "all_types" list.
            # if the type is not present in "all_types" we have to add it.
            there = next((item for item in all_types if item["type"] == t), False)

            if not there:
                to_insert = {"type": t, "count": 1, "score": elem[2]}
                all_types.append(to_insert)

            else:
                # if the type is already present we increment its counter and upgraded its score.
                # The update of the score is done differently depending on the type of the tweet
                # if it is one of the type twitted by the author of the tweet or not.
                present = next((item for item in p.get(author) if item[0] == t), False)
                if present:
                    couple = next(item for item in p.get(author) if item[0] == t)
                    print("Type " + t + " is present with prob. : " + str(couple[1]))
                    to_change = all_types[all_types.index(there)]
                    to_change["count"] = to_change["count"] + 1
                    print(t,to_change["score"])

                    # in the case the type is contained in the data-structure containing the
                    # probabilities we increment the score by considering the probabilities, so
                    # the overall score will be higher.
                    to_change["score"] = to_change["score"] + (elem[2]*(1 + (couple[1]*1000)))
                    print(t,to_change["score"])
                else:
                    to_change = all_types[all_types.index(there)]
                    to_change["count"] = to_change["count"] + 1
                    print(t, to_change["score"])

                    # if the type is not among the ones used by the author of the current tweet
                    # we update the score just by adding the score of the current node in the "common_nodes" list.
                    to_change["score"] = to_change["score"] + elem[2]
                    print(t, to_change["score"])

    #all_types = sorted(all_types, key=lambda i: (i['count'],i['score']), reverse=True)

    # "all_types" is sorted in decresing order of score
    all_types = sorted(all_types, key=lambda i: i['score'], reverse=True)

    #all_types = sorted(all_types, key=lambda i: i['count'], reverse=True)
    print(all_types)
    predicted_tag = ""

    # if all_types is empty we choose for the "Thing" class.
    if not all_types:
        predicted_tag = "Thing"

    # else we do the same consideration that we have done in the case of one node in common, we scan all types
    # by searching the one that is compatible with our classes. We extract the types from the top of "all_types"
    # since they are sorted in decreasing order of score, in that way we are sure to search first for the most
    # probable type for the tweet, if the type is not in "target_names" list, we pop it out, and we look for the others.
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

'''
THE ENTITIES HAVE NO NODE IN COMMON.
------------------------------------------------------
The parameters for the function are:

--> common nodes:...the list of common nodes;

--> target_names:...the list of the classes in our dataset; 

--> author:.........the author of the tweet;

--> p:..............the data-structure containing the probabilities, in particular it is a dict having as key the 
                    author names.
'''
def no_common_nodes_types(entities,inverted_index,target_names,author,p):
    first_nodes = list()
    all_types = list()
    not_in = False

    # for each entity in the tweet that we have extract we get the nodes from the index
    for e in entities:
        nodes = inverted_index.get(e)
        if nodes:
            # the nodes are sorted according to the score, from the highest to the lowest.
            nodes = sorted(inverted_index.get(e), key=lambda i: i["score"],reverse=True)

            # initially we pick only the first node.
            n1 = nodes[0]
            first_nodes.append(n1)

            # if we have more than one nodes, we take all the node of the lineage of that particular entities
            # in order to have more types to extract.
            if len(nodes) > 1:
                for n in nodes:
                    first_nodes.append(n)

    # "first_nodes" contains the nodes that we have decided to append.
    # If "first_nodes" has more than one single node...
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

                else:
                    # if the type is already present we increment its counter and upgraded its score.
                    # The update of the score is done differently depending on the type of the tweet
                    # if it is one of the type twitted by the author of the tweet or not.
                    present = next((item for item in p.get(author) if item[0] == t), False)
                    if present:
                        couple = next(item for item in p.get(author) if item[0] == t)
                        print("Type " + t + " is present with prob. : " + str(couple[1]))
                        to_change = all_types[all_types.index(there)]
                        to_change["count"] = to_change["count"] + 1
                        print(t, to_change["score"])

                        # in the case the type is contained in the data-structure containing the
                        # probabilities we increment the score by considering the probabilities, so
                        # the overall score will be higher.

                        # the only thing that changes here is how the score is retrieved from the element
                        # since "fist_nodes" stores the nodes of the index that are dictionaries, this is why
                        # we have the "get" method.
                        to_change["score"] = to_change["score"] + (elem.get('score')*(1 + (couple[1]*1000)))
                        print(t, to_change["score"])

                    else:
                        to_change = all_types[all_types.index(there)]
                        to_change["count"] = to_change["count"] + 1
                        print(t, to_change["score"])

                        # if the type is not among the ones used by the author of the current tweet
                        # we update the score just by adding the score of the current node in the "first_nodes" list.
                        to_change["score"] = to_change["score"] + elem.get('score')
                        print(t, to_change["score"])

        #all_types = sorted(all_types, key=lambda i: (i['count'],i['score']), reverse=True)

        # "all_types" is sorted in decresing order of score
        all_types = sorted(all_types, key=lambda i:  i['score'], reverse=True)

        #all_types = sorted(all_types, key=lambda i: i['count'], reverse=True)
        print(all_types)
        select_type = all_types
        predicted_tag = ""

        # same is in the case of multiple nodes
        while predicted_tag not in target_names:
            print(predicted_tag)
            if not select_type:
                not_in = True
                break

            predicted_tag = class_adjust(select_type[0].get('type'))
            select_type.pop(0)

        if not_in:
            #predicted_tag = all_types[0].get('type')
            #predicted_tag = "Thing"
            predicted_tag = max(p.get(author), key=lambda item: item[1])[0]

        # print("Sorted: " + str(all_types))

        return predicted_tag

    # if we have only node, for instance when we have only one entity in our
    # tweet and its lineage is composed of only one node.
    elif len(first_nodes) == 1:
        types = list(first_nodes[0].get("types"))
        score = first_nodes[0].get("score")
        print(types)

        # we remove "Thing" if present
        if "Thing" in types:
            types.remove("Thing")

        # for all types that are present in this node, we barely do the same of what we have done in multiple node case,
        # with the difference that we do not update the scores (since we are in the case of only one node), so in order
        # to get higher scores among the types we use the probabilities values.
        for t in types:
            present = next((item for item in p.get(author) if item[0] == t), False)
            if present:
                couple = next(item for item in p.get(author) if item[0] == t)
                to_insert = {"type": t, "count": 1, "score": score * (1 + (couple[1] * 1000))}
                all_types.append(to_insert)
            else:
                to_insert = {"type": t, "count": 1, "score": score}
                all_types.append(to_insert)

        # all_types = sorted(all_types, key=lambda i: (i['count'],i['score']), reverse=True)
        all_types = sorted(all_types, key=lambda i: i['score'], reverse=True)
        # all_types = sorted(all_types, key=lambda i: i['count'], reverse=True)
        print(all_types)
        select_type = all_types
        predicted_tag = ""

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

    # if the we are in the case in which the entities have empty lineages, we return the type with highest probability
    # for the author. This really helps the classifier and this choice is due the fact that in the case in which have no
    # nodes in common is difficult to establish which is the correct class and so is the part where the number of error
    # increases.
    else:
        #predicted_tag = "Thing"
        predicted_tag = max(p.get(author), key=lambda item: item[1])[0]
        return predicted_tag

'''
The "class_adjust" function takes as parameter the tag and in the case it is one of the type that can be collapsed it 
applies the following rules:

+  SportsOrganization,SportsTeam            -------->   Sports

+  MusicAlbum,MusicGroup,MusicRecording     -------->   Music

+  Book,BookSeries                          -------->   Book

+  EducationalOrganization,Organization,    -------->   Organization
   GovernmentOrganization
    
+  Movie,MovieSeries                        -------->   Movie

+  VideoGame,VideoGameSeries                -------->   VideoGame

+  Other                                    -------->   Leave as it is
'''
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

    elif tag in music:
        c = "Music"
        return c

    elif tag in organization:
        c = "Organization"
        return c

    elif tag in book:
        c = "Book"
        return c

    elif tag in movie:
        c = "Movie"
        return c

    elif tag in movie:
        c = "VideoGame"
        return c

    else:
        return tag

