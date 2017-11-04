#!/usr/bin/python
import spacy

from doc_metadata import DOCUMENT_INDEX
import outline

import pdb

class DocumentCollection:
    """
    This initializes a top-level collection of scipy documents. Object is to create
    one collection that can be used for organizing documents, together with the
    character offset indexes for the documents.

    First draft of object will read in all documents and reprocess. Later drafts
    will consist of an "initialization" object used to reinitialize raw documents,
    and a "persistence" object that reads the already-processed image from a file,
    either as processed by spacy, or in the case of indexes, "pickled."
    """

    DOC_FOLDER = "texts/"
    nlp = None    # alloted for NLP engine

    def __init__(self):
        """
        Initializes engine; reads and indexes everything.
        """
        self.nlp = spacy.load('en')    # use English

        for doc_obj in doc_metadata.DOCUMENT_INDEX:            
            # read in the text file you wish to analyze
            with open(DocumentCollection.DOC_FOLDER + doc_obj.file, 'r') as next_file:
                text = next_file.read()
                utext = unicode(text.decode('utf8'))   # important!!

                # create a documentation index
                doc_index = outline.DocumentIndex(utext)

                # tokenize and process the document into spacy document
                doc = nlp.tokenizer(utext)
                nlp.tagger(doc)
                nlp.parser(doc)
                nlp.entity(doc)

                doc_obj["index"] = doc_index
                doc_obj["nlpdoc"] = doc

                
    def simple_search(self, test_str):
        """
        Demonstration routine. This performs a spacy entity search throughout the
        corpus and returns the accumulation of matches, involving
        - quotation in context
        - document metadata
        This matches a single token, and ignores case
        """
        simple_matcher = Matcher(nlp.vocab)
        matcher.add_pattern("test", [{LOWER: "hello"}])
        for doc_obj in doc_metadata.DOCUMENT_INDEX:
            matches = matcher(doc_obj["nlpdoc"])

            
