---
layout: function
title: Ground truth
code_title: TypesExtraction.py
main: /wir_project/pages/ground
---
# Tags for tweets

```python
path = "myfile.csv"
#path of your dataset
trial = readCSV(path)
print(trial)

#taggedTweets will be the list of tagged tweets
taggedTweets = list()
count = 0
for tweet in trial:
    print("\nYou still have: " + str(len(trial) - count) + " tweets left")

    text = tweet.get('full_text')
    print("\nAUTHOR: " +  tweet.get('screen_name'))
    print("\nTWEET:\n" + text + "\n" )
    print("-" * 40)

    res = preprocessing(text)
    print("This are the entities obtained by preprocessing:")
    print(res)
    print("\nSUGGESTED TYPES:")
    print(getTypes(res))
```
### We use the function ```get_types``` of the ```KBfunctions.py``` to get the types of the tweet, in order to have some suggestions.
Once we have decided we have then to insert the type, that will be associated to the tweet.

```python
    print("-"*40)

    #propt to tag the tweet
    inputType = input("Enter tag for the tweet (one or more, if more us a \',\' )\n"
                      "If you want to quit, type \"STOP\": ")

    if inputType == "STOP":
        break

    labeledTweet = { 'id': tweet.get('id'),
                     'screen_name': tweet.get('screen_name'),
                     'created_at': tweet.get('created_at'),
                     'full_text': text,
                     'tag': inputType
    }

    count = count + 1
    taggedTweets.append(labeledTweet)
    print("-"*40)



print("\n")
print("*"*40)
print("\nThe labeled tweets are:\n")

count = 0

#recap of your labeling process
for elem in taggedTweets:
    count = count + 1
    print(str(elem.get('id')) + " | " + elem.get('full_text') + " | " + elem.get('tag'))

print("\nYOU HAVE LABELED " + str(count) + " TWEETS\n ")
print("Please check your work...\n")
decision = ""
```
We give the possibility to modify the tweet by writing the id of the tweet for which we want to change the selected tags.

```python
modify = input("Do you need to modify something? y/n: ")

#you can decide to modify something if you want
while modify == "y":
    decision = input("If you are not sure about one label, write the id of the tweet that you want to change.\n"
                     "Write \"OK\" if everything is good: ")
    if decision == "OK":
        break

    newLabel = input("Write the new label that you want (one or more, if more us a \',\' ): ")
    elem = next(item for item in taggedTweets if item["id"] == int(decision))
    text = elem.get('full_text')
    created_at = elem.get('created_at')
    screen_name = elem.get('screen_name')

    taggedTweets.remove(next(item for item in taggedTweets if item["id"] == int(decision)))

    toReplace = {
        'id': decision,
        'screen_name': screen_name,
        'created_at': created_at,
        'full_text':text,
        'tag': newLabel
    }
    taggedTweets.append(toReplace)
    print("The element:")
    print(print(str(toReplace.get('id')) + " | " + toReplace.get('full_text') + " | " + toReplace.get('tag')))
    print("Has been correctly added to the list\n.")

```
### Once we have done we save our work.

```python
save = input("Do you want to save your work? y/n: ")

if save == 'y':
    path = ""
    writeNewCSV(path,taggedTweets)

else:
    finalDecision = input("ARE YOU REALLY SURE TO NOT SAVE? y/n: ")
    if finalDecision == 'n':
        path = ""
        writeNewCSV(path, taggedTweets)
```