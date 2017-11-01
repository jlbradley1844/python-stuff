#!/usr/bin/python
import spacy
import re

import pdb

# read in the text file you wish to analyze
with open('texts/gleanings.txt', 'r') as myfile:
    text=myfile.read()
# set up spacy
import spacy
nlp = spacy.load('en')    # use English
# initialize the pipeline
# the Gutenberg text downloads are already in utf8, following is for python2
utext=unicode(text.decode('utf8'))
doc = nlp.tokenizer(utext)
# perform the pipeline processing
nlp.tagger(doc)
nlp.parser(doc)
nlp.entity(doc)

def get_headers(doc_string):
    """
    Headers in these documents are generally all-caps. That gives an indication
    of where the spans are. It will take the document as a string and return
    an array of tuples. Each tuple will be beginning and end character position
    of a header. len() of the returned array is the number of sections.
    """
    header=re.compile("(\r\n|^)[^a-z\r\n]+(\r\n|$)")
    matches=header.search(doc_string)
    header_pos = []
    tail=0
    while matches is not None:
        header_pos.append((tail + matches.span()[0], tail + matches.span()[1]))
        tail = tail + matches.span()[1]
        matches=header.search(doc_string[tail:])

    return header_pos

def get_paragraph_markers(doc_string):
    """
    Gets position of the paragraph breaks. A paragraph is at least two line feeds
    in a row
    """
    para=re.compile("\r\n(\r\n)+")
    matches=para.search(doc_string)
    marker_pos = []
    tail=0
    while matches is not None:
        marker_pos.append((tail + matches.span()[0], tail + matches.span()[1]))
        tail = tail + matches.span()[1]
        matches=para.search(doc_string[tail:])

    return marker_pos
    
foo1=get_headers(utext)
foo2=get_paragraph_markers(utext)
print foo1
print foo2
