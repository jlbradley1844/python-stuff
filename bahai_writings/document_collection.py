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

        for doc_obj in DOCUMENT_INDEX:            
            # read in the text file you wish to analyze
            with open(DocumentCollection.DOC_FOLDER +
                      DOCUMENT_INDEX[doc_obj]["file"], 'r') as next_file:
                text = next_file.read()
                utext = unicode(text.decode('utf8'))   # important!!

                # create a documentation index
                doc_index = outline.DocumentIndex(utext)

                # tokenize and process the document into spacy document
                doc = self.nlp.tokenizer(utext)
                self.nlp.tagger(doc)
                self.nlp.parser(doc)
                self.nlp.entity(doc)

                DOCUMENT_INDEX[doc_obj]["index"] = doc_index
                DOCUMENT_INDEX[doc_obj]["nlpdoc"] = doc


    def extract_doc(self, doc_index):
        """
        given the document tag, extract the document and all the metadata
        :param doc_index - document abbreviation
        """
        return DOCUMENT_INDEX[doc_index]


                
    def simple_search(self, match, doc=None):
        """
        Demonstration routine. This performs a spacy entity search throughout the
        corpus and returns the accumulation of matches, involving
        - quotation in context
        - document metadata
        @param matcher - may be a string or JSON-style dictionary. If a string, it will
        match a single token, and ignores case
        @param doc - if None, matches all documents. If supplied, must be mnemonic of
        the document being search. If array, will be the list of the documents.
        :returns - matcher output. This returns a 4-tuple array of elements consisting
        of (matchid, ?, start, end)
        """
        simple_matcher = spacy.matcher.Matcher(self.nlp.vocab)
        if type(match) == str:
            pattern = [{'LOWER': match}]
        else:
            pattern = match
        simple_matcher.add_pattern("test", pattern)
        matches = {}
        for doc_obj in DOCUMENT_INDEX:
            matches[doc_obj] = simple_matcher(DOCUMENT_INDEX[doc_obj]["nlpdoc"])

        return matches
            
