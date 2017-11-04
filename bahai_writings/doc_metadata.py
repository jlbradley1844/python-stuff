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
DOCUMENT_INDEX = {
    "GWB": {
        "file": "gleanings.txt",
        "full_name": "Gleanings from the Writings of Baháulláh",
        "pub_info": ("http://www.gutenberg.org/wiki/Bahá%27í_Faith_(Bookshelf),"
                     " downloaded October 10, 2017")
    },
    "SVFV": {
        "file": "seven-valleys-four-valleys.txt",
        "full_name": "Seven Valleys and the Four Valleys",
        "pub_info": ("http://www.gutenberg.org/wiki/Bahá%27í_Faith_(Bookshelf),"
                     " downloaded October 26, 2017")
    },
    "KI": {
        "file": "kitab-i-iqan.txt",
        "full_name": "Kitáb-i-Íqán",
        "pub_info": ("http://www.gutenberg.org/wiki/Bahá%27í_Faith_(Bookshelf),"
                     " downloaded October 26, 2017")
    },
    "PM": {
        "file": "prayers-and-meditations.txt",
        "full_name": "Prayers and Meditatons",
        "pub_info": ("http://www.gutenberg.org/wiki/Bahá%27í_Faith_(Bookshelf),"
                     " downloaded October 26, 2017")
    }
}
