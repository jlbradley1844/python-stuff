#!/usr/bin/python
"""
This is used by NLP code, but does not require any. This takes unicode
documents and produces document indexes that let you know what section
and paragraph a particular offset in the text is. That way, you know
which section the retrieved text is from.

This uses regular expressions to find the section and paragraph elements.
As of now, headers are recognized via an all-caps paragraph, and paragraphs
are recognized as two or more line feeds.
"""
import re

def sectioner(doc_string, regex):
    """
    Find all regex-identifiable elements in a document
    @param doc_string: UNICODE string containing dcoument in which elements are
    to be identified
    @param regex: compiled regexp expression to perform this match
    @returns: array of (begin, end) tuples, sorted. Each tuple is the beginning
    and ending character offset of the element found
    """
    matches=regex.search(doc_string)
    header_pos = []
    tail=0
    while matches is not None:
        header_pos.append((tail + matches.span()[0], tail + matches.span()[1]))
        tail = tail + matches.span()[1]
        matches=regex.search(doc_string[tail:])

    return header_pos


def get_headers(doc_string):
    """
    Headers in these documents are generally all-caps. That gives an indication
    of where the spans are. It will take the document as a string and return
    an array of tuples with character offsets for the strings.
    """
    HEADER_REGEX = re.compile("(\n|^)[^a-z\n]+(\n|$)")
    return sectioner(doc_string, HEADER_REGEX)


def get_paragraph_markers(doc_string):
    """
    Gets position of the paragraph breaks. A paragraph is at least two line feeds
    in a row
    """
    PARAGRAPH_REGEX = re.compile("\n(\n)+")
    return sectioner(doc_string, PARAGRAPH_REGEX)


def consolidate_headers(header_offsets):
    """
    This takes the array of headers and returns just the starting character of
    each header. These character offsets are used to section the document
    """
    return [x[0] for x in header_offsets]


def consolidate_paragraphs(paragraph_offsets, header_offsets):
    """
    This takes the array of paragraphs and returns point at which paragraph begins. 
    NOTE that  for purposes of paragraphs, headers are counted as being within the
    paragraph following it
    """
    # pragmatically, both of these offsets will start at 0
    cleaned_para_list = [0]
    prior_para_marker = 0
    header_ptr = 0
    
    for para_marker in paragraph_offsets:
        if header_ptr >= len(header_offsets):
            # no more headers. All remaining paragraphs under last heading
            cleaned_para_list.append(para_marker[0])
        else:
            if (header_offsets[header_ptr][0] >= prior_para_marker and
                header_offsets[header_ptr][1] <= para_marker[1]):
                # header is "merged" into this paragraph, so don't
                # add the next paragraph marker, just mvoe along
                header_ptr = header_ptr + 1
            else:
                # header isn't up yet, so this paragraph marker is valid
                cleaned_para_list.append(para_marker[0])
        prior_para_marker = para_marker[0]

    return cleaned_para_list
        

def binary_lookup(index, offsets):
    """
    Given a character index, look up the index of it in the offsets. This will
    be the number at which the next index is greater
    """
    bottom = 0
    top = len(offsets) - 1
    if index > offsets[top]:
        return top
    
    while top - bottom > 1:
        mid = (top + bottom) // 2
        if index >= offsets[mid]:
            bottom = mid
        else:
            top = mid

    return bottom


class DocumentIndex:
    """
    This class is initialized by a document. It takes a unicode string as a
    document and initializes the header and paragraph marker locations. It then
    provides a get_index which will return information about paragraph markers
    and header sections for a given offset
    NOTE: offsets returned by the DocumentIndex are CHARACTER-BASED. That is different
    than the offsets from extracting spacy's Span object, which are TOKEN-BASED. As
    such, it is only useful for finding offsets in the original string object itself.
    """

    header_offsets = []
    header_values = []
    paragraph_offsets = []

    def __init__(self, docstring):
        raw_header_offsets = get_headers(docstring)
        self.header_offsets = consolidate_headers(raw_header_offsets)

        raw_paragraph_offsets = get_paragraph_markers(docstring)
        self.paragraph_offsets = consolidate_paragraphs(raw_paragraph_offsets, raw_header_offsets)

        for hdr_span in raw_header_offsets:
            self.header_values.append(docstring[hdr_span[0]:hdr_span[1]].strip())   # lop off EOL

    def lookup(self, offset):
        """
        returns information on the location at which a location is
        :param offset - character offset about which we want the location
        information.
        :returns a dictionary with three fields
        "section" - reference to the current section header (a string)
        "paragraph" - reference to numbered paragraph in which offset is present
        "section_seq" - reference to numbered section in which offset is present
        """
        section_index = binary_lookup(offset, self.header_offsets)
        paragraph_index = binary_lookup(offset, self.paragraph_offsets)
        return {
            "section": self.header_values[section_index],
            "paragraph": paragraph_index + 1,
            "section_seq": section_index + 1
            }


    def get_paragraph_span(self, para_num):
        """
        returns the character offsets associated with a given paragraph
        in a (begin,end) tuple. if this is the last paragraph, None is
        returned for end, indicating that we will take the span through the end.
        """
        begin = self.paragraph_offsets[para_num - 1]
        end = None
        if para_num < len(self.paragraph_offsets):
            end = self.paragraph_offsets[para_num]

        return (begin, end)


    def get_number_of_paragraphs(self):
        """
        returns the number of paragraphs in document
        """
        return len(self.paragraph_offsets)

    
    def get_section_span(self, section_seq):
        """
        return the character offsets associated with a given section in
        a begin, end tuple. If this is the last section, None is returned
        for end, indicating one should take the span through the end.
        """
        begin = self.header_offsets[section_seq - 1]
        end = None
        if section_seq < len(self.header_offsets):
            end = self.header_offsets[section_seq]

        return (begin, end)


    def get_number_of_sections(self):
        """
        returns the number of sections in document
        """
        return len(self.header_offsets)
