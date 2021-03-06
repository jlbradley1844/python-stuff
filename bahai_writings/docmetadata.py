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
    # Category: Baha'u'llah
    "ESW": {
        "category": "Baha'u'llah",
        "file": "epistle-son-wolf.txt",
        "full_name": "Epistle to the Son of the Wolf",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "GDM": {
        "category": "Baha'u'llah",
        "file": "gems-of-divine-mysteries.txt",
        "full_name": "Gems of Divine Mysteries",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "GWB": {
        "category": "Baha'u'llah",
        "file": "gleanings.txt",
        "full_name": "Gleanings from the Writings of Bahá’u’lláh",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 10, 2017")
    },
    "HW": {
        "category": "Baha'u'llah",
        "file": "hidden-words.txt",
        "full_name": "The Hidden Words of Bahá’u’lláh",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 10, 2017")
    },
    "KA": {
        "category": "Baha'u'llah",
        "file": "kitab-i-aqdas.txt",
        "full_name": "The Kitáb-i-Aqdas",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 10, 2017")
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
        "full_name": "Prayers and Meditations",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "SLH": {
        "category": "Baha'u'llah",
        "file": "summons-of-lord.txt",
        "full_name": "Summons of the Lord of Hosts",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "SVFV": {
        "category": "Baha'u'llah",
        "file": "seven-valleys-four-valleys.txt",
        "full_name": "Seven Valleys and the Four Valleys",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    },
    "TB": {
        "category": "Baha'u'llah",
        "file": "tablets-of-bahaullah.txt",
        "full_name":  "Tablets of  Bahá’u’lláhRe vealed after the Kitáb-i-Aqdas",
        "pub_info": ("https://www.gutenberg.org/wiki/Bah%C3%A1%27%C3%AD_Faith_%28Bookshelf%29",
                     " downloaded October 26, 2017")
    }
    # category: Abdu'l-Baha

}
