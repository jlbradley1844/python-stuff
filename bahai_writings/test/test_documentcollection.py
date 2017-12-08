#!/usr/bin/python
from globalnlpengine import GLOBAL_NLP_ENGINE
from documentcollection import DocumentCollection
from docmetadata import DOCUMENT_INDEX
import pytest

@pytest.fixture(scope="module")
def obj_test():
    """
    Spacy documents take a while to create from scratch. To allow extensive
    API testing, it is necessary to create the master documentation object
    from scratch, but we want to do it just once and share between tests. 
    Because the document only contains read-only methods, there is no
    complications caused by object reuse.

    It takes one small document and one larger one: Seven Valleys and Gleanings
    """
    LOCAL_COLLECTION = {}
    LOCAL_COLLECTION["GWB"] = DOCUMENT_INDEX["GWB"]
    LOCAL_COLLECTION["SVFV"] = DOCUMENT_INDEX["SVFV"]
    
    return DocumentCollection(LOCAL_COLLECTION, GLOBAL_NLP_ENGINE)
    

def test_matching(obj_test):
    """
    This performs some simple tess on a subset document collection. 
    """
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

