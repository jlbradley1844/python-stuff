#!/usr/bin/python
from documentcollection import DocumentCollection
from docmetadata import DOCUMENT_INDEX
from docutility import DocUtility, DegenerateSelection
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

    #continue
    next_selection = doc_utility.get_next_scoped_selection(doc[1230:1233],
                                                           DocUtility.PARAGRAPH)
    assert next_selection[1] == DocUtility.SEGMENT
    assert doc_utility.clean_whitespace(next_selection[0])[0:99] == (
        u"It is incumbent on these servants that they cleanse the heart\u2014which "
        "is the wellspring of divine tre")
    assert len(next_selection[0]) == 1312
    
    #continue
    next_selection = doc_utility.get_next_scoped_selection(doc[1230:1233],
                                                           DocUtility.SEGMENT)
    assert next_selection[1] == DocUtility.EXP_SEGMENT
    assert doc_utility.clean_whitespace(next_selection[0])[0:99] == (
        u"The Valley of Search The steed of this Valley is patience; without "
        "patience the wayfarer on this jo")
    assert len(next_selection[0]) == 2663
    assert next_selection[1] == DocUtility.EXP_SEGMENT

    threw_execept = False
    try:
        next_selection = doc_utility.get_next_scoped_selection(doc[1230:1233],
                                                           DocUtility.EXP_SEGMENT)
    except DegenerateSelection:
        threw_except = True
    assert threw_except

    # heading on SVFV doesn't really apply, so you get degenerate selection anyways
    threw_execept = False
    try:
        next_selection = doc_utility.get_next_scoped_selection(doc[1230:1233],
                                                               DocUtility.EXP_SEGMENT, True)
    except DegenerateSelection:
        threw_except = True
    assert threw_except   # no section, so it did throw
    # the whole freakin' valley of search
    assert doc_utility.clean_whitespace(next_selection[0])[0:99] == (
        u"THE SEVEN VALLEYS OF BAH\xc1\u2019U\u2019LL\xc1H _In the Name of God, "
        "the Clement, the Merciful._ Praise be to God ")
    assert len(next_selection[0]) == 63978
    assert next_selection[1] == DocUtility.DOCUMENT
        
        
