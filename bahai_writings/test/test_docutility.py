#!/usr/bin/python
from documentcollection import DocumentCollection
from docmetadata import DOCUMENT_INDEX
from docutility import DocUtility
from outline import DocumentIndex
import pytest

import pdb

def test_doc_extract():
    """
    This performs collapse/expand options on one of the shorter documents
    """
    LOCAL_COLLECTION = {}
    LOCAL_COLLECTION["SVFV"] = DOCUMENT_INDEX["SVFV"]    
    obj_test = DocumentCollection(LOCAL_COLLECTION)
    doc_obj = obj_test.extract_doc("SVFV")
    doc = doc_obj["nlpdoc"]
    raw_text = doc_obj["raw"]
    index = doc_obj["index"]

    doc_utility = DocUtility(index, raw_text)
    raw_sentence = doc_utility.get_scoped_selection(doc[1230:1233], DocUtility.SENTENCE)
    sentence = doc_utility.clean_whitespace(raw_sentence)
    assert sentence == ("At every step, aid from the Invisible Realm will "
                        "attend him and the heat of his search will grow.")

    # now test a paragraph
    raw_paragraph = doc_utility.get_scoped_selection(doc[1230:1233], DocUtility.PARAGRAPH)
    paragraph = doc_utility.clean_whitespace(raw_paragraph)
    assert len(paragraph)==600
    assert paragraph[0:99] == ("In this journey the seeker reacheth a stage wherein he "
                               "seeth all created things wandering distracted in search "
                               "of the Friend. How many a Jacob will he see, hunting after")[0:99]

    # bump it up from the specific sentence
    next_selection = doc_utility.get_next_scoped_selection(doc[1230:1233],
                                                           DocUtility.SENTENCE)
    assert next_selection[1] == DocUtility.PARAGRAPH
    assert doc_utility.clean_whitespace(next_selection[0])[0:99] == (
        ("In this journey the seeker reacheth a stage wherein he "
         "seeth all created things wandering distracted in search "
         "of the Friend. How many a Jacob will he see, hunting after")[0:99])

