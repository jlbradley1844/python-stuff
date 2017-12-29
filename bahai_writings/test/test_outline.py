#!/usr/bin/python
import outline
import pytest
import pdb

def test_headerdetect():
    with open('texts/gleanings.txt', 'r', encoding='utf8') as myfile:
        text=myfile.read()

    out = outline.get_headers(text[0:30000])
    assert out == [(0, 48), (3005, 3058), (3307, 3360), (4850, 4904),
        (5875, 5925), (9330, 9382), (10949, 11005), (12252, 12305),
	(12707, 12759), (13864, 13914), (15695, 15750), (19997, 20054),
	(20250, 20303)]

    out = outline.get_headers(text)
    assert len(out) == 166

    nxt = outline.get_headers(text[:100000])
    out2 = outline.consolidate_headers(nxt)
    assert out2 == [0, 3005, 3307, 4850, 5875, 9330, 10949, 12252,
        12707, 13864, 15695, 19997, 20250, 35402, 46565, 51136, 53067,
	57299, 62211, 65661, 66530, 67664, 76344, 80506, 81373, 81950,
	88151, 94252, 96301]
    
    
def test_paragraphdetect():
    with open('texts/gleanings.txt', 'r', encoding='utf8') as myfile:
        text=myfile.read()

    out = outline.get_paragraph_markers(text[0:10000])
    assert out == [(47, 50), (349, 351), (1081, 1083), (1806, 1808),
        (2290, 2292), (2706, 2708), (3000, 3006), (3057, 3060),
	(3302, 3308), (3359, 3362), (3846, 3848), (4845, 4851),
	(4903, 4906), (5585, 5587), (5870, 5876), (5924, 5927),
	(6342, 6344), (7488, 7490), (7879, 7881), (8205, 8207),
	(8667, 8669), (9325, 9331), (9381, 9384), (9845, 9847)]

    
def test_paraindex():
    with open('texts/gleanings.txt', 'r', encoding='utf8') as myfile:
        text=myfile.read()

    hspans = outline.get_headers(text[:10000])
    hout = outline.consolidate_headers(hspans)
    pspans = outline.get_paragraph_markers(text[:10000])
    pout = outline.consolidate_paragraphs(pspans, hspans)
    assert pout == [0, 349, 1081, 1806, 2290, 2706, 3000, 3302, 3846,
        4845, 5585, 5870, 6342, 7488, 7879, 8205, 8667, 9325, 9845]


def test_lookup():
    arr = [0, 349, 1081, 1806, 2290, 2706, 3000, 3302, 3846,
        4845, 5585, 5870, 6342, 7488, 7879, 8205, 8667, 9325]
    assert len(arr) == 18
    
    assert outline.binary_lookup(0, arr) == 0
    assert outline.binary_lookup(4000, arr) == 8
    assert outline.binary_lookup(1000000, arr) == 17
    assert outline.binary_lookup(3365, arr) == 7


def test_indexer():
    with open('texts/gleanings.txt', 'r', encoding='utf8') as myfile:
        text=myfile.read()

    doc = outline.DocumentIndex(text)
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
        "paragraph": 19,
        "section_seq": 6
        }
    assert doc.lookup(100000) == {
        "section": "XXIX: THE PURPOSE OF GOD IN CREATING MAN HATH...",
        "paragraph": 132,
        "section_seq": 29
        }
    # overflow - point to terminal datum??
    assert doc.lookup(500000) == {
        "section": "CLXVI: WHOSO LAYETH CLAIM TO A REVELATION DIRECT...",
        "paragraph": 718,
        "section_seq": 166
        }


def test_simple_getters():
    with open('texts/gleanings.txt', 'r', encoding='utf8') as myfile:
        text=myfile.read()
    doc = outline.DocumentIndex(text)

    assert doc.get_number_of_paragraphs() == 718
    assert doc.get_number_of_sections() == 166


def test_para_getter():
    with open('texts/gleanings.txt', 'r', encoding='utf8') as myfile:
        text=myfile.read()
    doc = outline.DocumentIndex(text)

    span = doc.get_paragraph_span(2)
    assert span == (349, 1081)


def test_sect_getter():
    with open('texts/gleanings.txt', 'r', encoding='utf8') as myfile:
        text=myfile.read()
    doc = outline.DocumentIndex(text)

    span = doc.get_section_span(4)
    assert span == (4850, 5875)

