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
    index = doc_obj["index"]

    doc_utility = DocUtility(doc, index)
    raw_sentence = doc_utility.get_scoped_selection((1230,1233), DocUtility.SENTENCE)
    sentence = doc_utility.clean_whitespace(raw_sentence)
    assert sentence == ("At every step, aid from the Invisible Realm will "
                        "attend him and the heat of his search will grow.")
