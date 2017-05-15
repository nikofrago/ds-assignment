# ds-assignment
Python app to calculate top terms and top relationships from a corpus of people's short bios

## REQUIREMENTS
Python 2.7 is the only version tested so it is highly recommended.
The file `requirements.txt` contains the modules required to run the app.
To install the required modules execute
```
pip install -r requirements.txt
```
## START
Upon successful installation of the required modules,
the web server can be started by executing
```
python app.py
```
in the project root directory
## USAGE
The server listens to the following url:
```
http://127.0.0.1:5000
```
### Top 10 terms
In oder to get the top 10 terms for a person on the dataset request:
```
http://127.0.0.1:5000/top10words/<name>
e.g.
http://127.0.0.1:5000/top10words/Arnold Schwarzenegger
{
  "name": "Arnold Schwarzenegger", 
  "top 10 words": [
    "schwarzenegger", 
    "terminator", 
    "governor", 
    "bodybuilding", 
    "term", 
    "boxoffice", 
    "2015", 
    "recall", 
    "oak", 
    "2011schwarzenegger"
  ]
}
```
where <name> is the name of the person
If <name> is not provided, a random person will be picked:
```
http://127.0.0.1:5000/top10words/
```
### Top 10 relationships
In oder to get the top 10 relationships for a person on the dataset request:
```
http://127.0.0.1:5000/top10relationships/<name>
```
where <name> is the name of the person
If <name> is not provided, a random person will be picked:
```
http://127.0.0.1:5000/top10relationships/
e.g. 
http://127.0.0.1:5000/top10relationships/Barack Obama
{
  "name": "Barack Obama", 
  "top 10 relationships": [
    "Barack Obama", 
    "Joe Biden", 
    "Lauro Baja", 
    "Hillary Rodham Clinton", 
    "Chris Redfern", 
    "Barry Sullivan (lawyer)", 
    "Kcho", 
    "M. Cherif Bassiouni", 
    "Joe Lieberman"
  ]
}
```
## How it works
The model is based on the well-established representation called TF-IDF of a corpus of documents.
Each document gets broken up into words (determined by whitespace) and these are then counted and added to a 'bag' (hence, bag-of-words, an alternative name for this representation).
The word count constitutes the Term Frequency (TF) part of the representation.
The higher the count of a word, the more representative of the document it belongs to is.
However, in most languages, and, certainly, in English, there exist many words that appear very frequently but are not specific to the document that contains them. E.g. 'and', 'in', etc.
These are known as 'stop-words' and have been removed from the counts for this exercise.
Furthermore, across the corpus, some words appear more frequently than others, thus having a more generic, less document-specific association.
In order to deal with this, a weighting term called Inverse Document Frequency (IDF) is introduced which penalises words that occur frequently across the corpus and rewards infrequent words.
The formula for the IDF is 
![](tfidf.gif?raw=true)

We can thus calculate the each document's TFIDF and get the top 10 values as the top 10 terms of the person in question.
this is proveided by the api call
```
http://127.0.0.1:5000/top10words/
```
The TFIDF thus allows us to create a structured, numerical representation of each document in the corpus. From this point we can start performing statistical operations on the documents.
In order to establish the relationship between two documents, we can utilise the `cosine similarity` metric. As we have effectively converted eaach document into a vector, we can take the dot product between each pair and determine how similar the documents are.
Cosine similarity works like this
![](cosine.jpg?raw=true)
We can thus calculate the cosine similarity between each document and the other documents in the corpus and get the top 10 values as the top 10 relationships of the person in question.
this is proveided by the api call
```
http://127.0.0.1:5000/top10relationships/
```
