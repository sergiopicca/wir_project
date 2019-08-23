---
layout: function
title: Ground truth
code_title: EnterRepresentingTag.py
main: /wir_project/pages/ground
---
# Decide for the most representative tag

This time the .csv file will be write during the classification, since if there is some problem part of the file will be already written, you just need to put the right path to your labeled datset, the one obtained by tagging the tweet with one or more tag.

At the end you will have one final .csv file called "one_label_data.csv" with all previous field and 
a new field representing the final tag.

```python
path = "mymultitag.csv"
tweet_list = readLabeledCSV(path)

final_labeled_data = list()
count = 0
file = "one_label_data.csv"


with open(file, 'w') as writeFile:
    writer = csv.writer(writeFile)
    fieldnames = ['id', 'screen_name', 'created_at','full_text','tag', 'repr_tag']
    writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
    writer.writeheader()

    for tweet in tweet_list:
        print("\nYou still have: \n" + str(len(tweet_list) - count))
        count = count + 1
        print("TWEET:\n")
        print(tweet.get('full_text')[:90] + "\n" + tweet.get('full_text')[90:])
        print('-'*40)
        print("The tags are: " + tweet.get('tag'))
        print('-'*40)

        tag = input("\nCHOOSE THE MOST REPRESENTATITVE TAG for the tweet: ")
        decision = input("Is \"" + tag + "\" your final decision?(y/n): ")

        while decision != "y":
            tag = input("\nCHOOSE THE MOST REPRESENTATITVE TAG for the tweet: ")
            decision = input("Is \"" + tag + "\" your final decision?(y/n): ")

        if decision == "y":
            writer.writerow(
                {'id': tweet.get('id'), 'screen_name': tweet.get('screen_name'), 'created_at': tweet.get('created_at'),
                 'full_text': tweet.get('full_text'), 'tag': tweet.get('tag'), 'repr_tag': tag})
        else:
            print("Wrong answer.")


writeFile.close()



```