#!/usr/bin/python
from documentcollection import DocumentCollection
from docmetadata import DOCUMENT_INDEX
import pytest

import pdb

def test_matching():
    """
    This performs some simple tess on a subset document collection. It
    takes one small document and one larger one: Seven Valleys and Gleanings
    """
    LOCAL_COLLECTION = {}
    LOCAL_COLLECTION["GWB"] = DOCUMENT_INDEX["GWB"]
    LOCAL_COLLECTION["SVFV"] = DOCUMENT_INDEX["SVFV"]
    
    obj_test = DocumentCollection(LOCAL_COLLECTION)
    ret_coll = obj_test.simple_search("search")
    for indx in ret_coll:
        doc_info = obj_test.extract_doc(indx)
        # the raw text can be found thusly:
        #doc_info["nlpdoc"][offset1:offset2]
        # you can also use
        #doc_info["nlpdoc"][offset1:offset2].sent
        # to print out the sentence in which it is found
        print doc_info["full_name"]
        for fnd in ret_coll[indx]:
            begin=fnd[2]
            end=fnd[3]
            print (doc_info["index"].lookup(begin)["section"] + ", paragraph " +
                   str(doc_info["index"].lookup(begin)["paragraph"]))
            print doc_info["nlpdoc"][begin:end].sent
            assert doc_info != None
