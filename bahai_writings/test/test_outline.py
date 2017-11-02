#!/usr/bin/python
import outline
import pytest

def test_headerdetect():
    with open('texts/gleanings.txt', 'r') as myfile:
        text=myfile.read()
    utext=unicode(text.decode('utf8'))

    out = outline.get_headers(utext[0:30000])
    assert out == [(0, 49), (3061, 3116), (3375, 3430),  (4948, 5004),
                   (5996, 6048),  (9514, 9568),  (11166, 11224),  (12497, 12552),
                   (12966, 13020),  (14147, 14199),  (16012, 16069),
                   (20387, 20446),  (20651, 20706)]

    out = outline.get_headers(utext)
    assert len(out) == 166

    nxt = outline.get_headers(utext[:100000])
    out2 = outline.consolidate_headers(nxt)
    assert out2 == [0, 3061,  3375,  4948,  5996,  9514,  11166,  12497,  12966,
                    14147,  16012,  20387,  20651,  36036,  47387,  52036,  54005,
                    58312,  63312,  66824,  67713,  68870,  77692,  81924,  82811,
                    83403,  89702,  95903,  97990]
    
    
def test_paragraphdetect():
    with open('texts/gleanings.txt', 'r') as myfile:
        text=myfile.read()
    utext=unicode(text.decode('utf8'))

    out = outline.get_paragraph_markers(utext[0:10000])
    assert out == [(47, 53),  (356, 360),  (1100, 1104),  (1836, 1840),  (2328, 2332),
                   (2751, 2755),  (3051, 3063),  (3114, 3120),  (3365, 3377),
                   (3428, 3434),  (3924, 3928),  (4938, 4950),  (5002, 5008),
                   (5696, 5700),  (5986, 5998),  (6046, 6052),  (6472, 6476),
                   (7635, 7639),  (8033, 8037),  (8365, 8369),  (8835, 8839),
                   (9504, 9516),  (9566, 9572)]

    
def test_paraindex():
    with open('texts/gleanings.txt', 'r') as myfile:
        text=myfile.read()
    utext=unicode(text.decode('utf8'))

    hspans = outline.get_headers(utext[:10000])
    hout = outline.consolidate_headers(hspans)
    pspans = outline.get_paragraph_markers(utext[:10000])
    pout = outline.consolidate_paragraphs(pspans, hspans)
    assert pout == [0, 356, 1100, 1836, 2328, 2751, 3051, 3365, 3924, 4938, 5696, 5986,
                   6472, 7635, 8033, 8365, 8835, 9504]


def test_lookup():
    arr = [0, 356, 1100, 1836, 2328, 2751, 3051, 3365, 3924, 4938, 5696, 5986,
                   6472, 7635, 8033, 8365, 8835, 9504]
    assert len(arr) == 18
    
    assert outline.binary_lookup(0, arr) == 0
    assert outline.binary_lookup(4000, arr) == 8
    assert outline.binary_lookup(1000000, arr) == 17
    assert outline.binary_lookup(3365, arr) == 7


def test_indexer():
    with open('texts/gleanings.txt', 'r') as myfile:
        text=myfile.read()
    utext=unicode(text.decode('utf8'))

    doc = outline.DocumentIndex(utext)
    assert doc.lookup(100) == {
        "section": "I: LAUDED AND GLORIFIED ART THOU, O LORD, MY...",
        "paragraph": 1,
        "section_seq": 1
        }
    assert doc.lookup(1000) == {
        "section": "I: LAUDED AND GLORIFIED ART THOU, O LORD, MY...",
        "paragraph": 2,
        "section_seq": 1
        }
    assert doc.lookup(10000) == {
        "section": "VI: BEHOLD, HOW THE DIVERS PEOPLES AND KINDREDS...",
        "paragraph": 18,
        "section_seq": 6
        }
    assert doc.lookup(100000) == {
        "section": "XXIX: THE PURPOSE OF GOD IN CREATING MAN HATH...",
        "paragraph": 129,
        "section_seq": 29
        }
    # overflow - point to terminal datum??
    assert doc.lookup(500000) == {
        "section": "CLXVI: WHOSO LAYETH CLAIM TO A REVELATION DIRECT...",
        "paragraph": 718,
        "section_seq": 166
        }
