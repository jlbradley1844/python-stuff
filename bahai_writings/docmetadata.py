#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

"""
This is a JSON-style index of the documents. All documents are held in the
text/ directory. If you add a document, you must add an entry in this
file, along with the metadata indicated.

The following metadata must be used:

STANDARD ABBREVIATION: the standard canonical abbreviation is the dictionary key.
The standard abbrevation must be used for Baha'i wrigings, as per
http://bahai-library.com/abbreviations_bahai_writings
must be used as the index to the structure. (This is going to be arbitrary,
so might as well make it standard!). Other nonstandard documents added should use
their own short mnemonic. Remember, your goal is to make it memorable, unique, and
easy to type!

file: file name. All files must be in text
full_name: Full title of document
remainder tbd

"""

CATEGORIES = [
    "Baha'u'llah",
    "Abdul-Baha",
    "Shoghi_Effendi",
    "UHJ",
    "Bible",
    "Koran"
    ]

    
DOCUMENT_INDEX = {
    "SVFV": {
        "category": "Baha'u'llah",
        "file": "seven-valleys-four-valleys.txt",
        "full_name": "Seven Valleys and the Four Valleys",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "KI": {
        "category": "Baha'u'llah",
        "file": "kitab-i-iqan.txt",
        "full_name": "The Kitáb-i-Íqán",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "PM": {
        "category": "Baha'u'llah",
        "file": "prayers-and-meditations.txt",
        "full_name": "Prayers and Meditatons",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "GWB": {
        "category": "Baha'u'llah",
        "file": "gleanings.txt",
        "full_name": "Gleanings from the Writings of Bahá’u’lláh",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 10, 2017")
    }
}
