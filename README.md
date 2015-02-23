BlabberBot
==========

A Twitter bot that just won't be quiet.

###Creating the config file.

Blabberbot requires there to be a config file named "blabberbot.cfg" to be included in the base directory. Below can be
copy and pasted into a text file.

```
[Twitter]
token = <Twitter Token>
token_secret = <Twitter Token Secret>
consumer = <Consumer Token>
consumer_secret = <Consumer Token Secret>

[Neo4j]
user = <GraphStory Username>
password = <GraphStory Password>
host = <GraphStory Host URL>

[Dictionary]
dict_key = <Merriam Webster Collegiate Dictionary Key>
thes_key = <Merriam Webster Thesaurus Key>
```