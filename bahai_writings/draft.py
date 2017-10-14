import spacy

# read in the text file you wish to analyze
with open('gleanings.txt', 'r') as myfile:
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
