---
layout: default
title: Ground truth
code_title: TypesExtraction.py - EnterRepresentingTag.py
---

# We need a ground truth
 
## Our dataset is composed of unlabeled tweets since we retrieved them thanks to Twitter APIs. We need to manually label the tweet.
### The idea

In the GKG we have a lot of types for different entities from the most general to the most specific, such as "Thing",Movie","MovieSeries","EducationalOrganization" and so on. The idea was to use the information present in the KB, so for each tweet we use the functions in the ```KBfunctions.py``` to propose the best types for each tweet than each of us manually decide which is the best from the one returned or select another one from the types of the GKG.

### We splitted the dataset in three to be fair
1. First we decide to assign one or more type for the tweet. [See the code](/wir_project/pages/ground/extraction)
2. We select only one type. [See the code](/wir_project/pages/ground/represent)