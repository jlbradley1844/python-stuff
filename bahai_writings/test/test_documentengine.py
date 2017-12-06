#!/usr/bin/python
from documentengine import DocumentEngine

import pytest

import pdb

@pytest.fixture(scope="module")
def obj_test():
    """
    Primary document engine for searches. NOTE THAT THIS MAY BE THE ONLY OBJECT DIRECTLY
    USED, AS THE PURPOSE OF THIS SCRIPT IS TO ENSURE ITS COMPLETENESS.

    Currently, I'm not using the "session" logic so there is no need to worry
    about sharing state. Once I start testing that, I will not be able to reuse the
    same document engine between the tests (at least not without planning)
    """
    return DocumentEngine()


def test_engine_helpers(obj_test):
    """ Tests various trivial helper functions """
    foo1 = obj_test.get_categories()
    assert foo1 == ["Baha'u'llah", 'Abdul-Baha', 'Shoghi_Effendi', 'UHJ', 'Bible', 'Koran']
    

    foo2 = obj_test.get_document_tags()
    assert foo2 == [{'category': "Baha'u'llah", 'tag': 'GWB'},
                    {'category': "Baha'u'llah", 'tag': 'KI'},
                    {'category': "Baha'u'llah", 'tag': 'SVFV'},
                    {'category': "Baha'u'llah", 'tag': 'PM'}]

    foo3 = obj_test.get_meatadata("PM")


def test_engine_search(obj_test):
    """ General test of simple search function """
    pdb.set_trace()
    foo4 = obj_test.simple_search(["find"], ["KI"])


def test_engine_navigation(obj_test):
    """ Test of selection expansion """
    pdb.set_trace()
    foo5 = obj_test.expand_selection("GWB", 1000)
    
