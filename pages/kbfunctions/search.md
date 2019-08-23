---
layout: function
title: Search function
code_title: KBfunctions.py - search
main: /wir_project/pages/kb
---

# Where all started...
## This is a very simple function that submit a query to the our KB
This is the function that contains some of the code provided from the original page of the [Google Knowledge Graph API](https://developers.google.com/knowledge-graph/). There is the ```api_key``` variable that contains the key to access the API. 

The ```query``` is a variable containing the actual keyword that we want to search.
```python
def search(query):
    api_key = ""
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    limit = 50
    params = {
        'query': query,
        'limit': limit,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())

    return response
```
The function return a ```.json``` file, that contains all the nodes retrieved from the GKG.