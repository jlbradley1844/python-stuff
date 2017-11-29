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
    pdb.set_trace()
    LOCAL_COLLECTION = {}
    LOCAL_COLLECTION["SVFV"] = DOCUMENT_INDEX["SVFV"]    
    obj_test = DocumentCollection(LOCAL_COLLECTION)
    doc = obj_test.extract_doc("SVFV")
    index = DocumentIndex(str(doc))

    doc_utility = DocUtility(doc, index)
    sentence = doc_utility.get_scoped_selection((30,33), DocUtility.SENTENCE)
    assert sentence == "now is the time for all good men to come to the aid of their party"
