#!/usr/bin/python
import spacy
from outline import DocumentIndex

class DegenerateSelection(Exception):
    """
    This is thrown in conjunction with the getters below. If you call a
    getter and it is equal to the next-smaller selection, rather than return
    the value, perform a throw to indicate that selection really doesn't exist
    as requested. e.g. if you have a one-paragraph document, segment, expseg
    and sect don't really exist.
    """
    pass
    

class DocUtility(object):
    """
    Class to wrap various on documents, mostly having to do with lookups and indexing
    """

    # Defined values of the document search scope
    SENTENCE = "sent"
    PARAGRAPH = "para"
    SEGMENT = "segment"
    EXP_SEGMENT = "expseg"
    SECTION = "sect"
    DOCUMENT = "doc"

    BASE_SEGMENT_DEF = 1   # Segment size of 3 paragraphs: #elements in [-1:1]
    EXP_SEGMENT_DEF = 3    # expanded segment size of 7 paragraphs: # elements in [-3:3]


    def __init__(self, doc, index):
        """
        :param docu - spacy document
        :param index - DocumentIndex object describing doc
        """
        self.doc = doc
        self.index = index


    def _get_sentence(self, token_ref):
        """
        Get the sentence a given token reference offset is in
        :param token_ref - numerical offset of token in document
        :returns the sentence of text cotaining the token_ref at the offset
        """
        return self.doc[token_ref[0]:token_ref[1]].sent


    def _get_paragraph_range(self, start_para, end_para = None):
        """
        Get the token offset range bounding one or more paragraphs in a range from the document
        :param start_para - Starting paragraph number to retrieve
        :param end_para - ending paragraph number.
        :returns tuple for (begin, end) token offsets. If end=None, then this means
        all text from begin and beyond should be fetched.
        """
        begin = index.get_paragraph_span(start_para)[0]
        end = index.get_paragraph_span(end_para)[1]
        return (begin, end)
        
        
        
    def _get_paragraph(self, token_ref):
        begin_reference = self.index.lookup(token_ref[0])
        end_reference = self.index.lookup(token_ref[1])
        start_par = begin_reference["paragraph"]
        end_par = end_reference["paragraph"]
        # look up token offsets for current paragraph
        (begin, end) = self._get_paragraph_range(start_par, end_par)
        if end is None:
            paragraph = self.doc[begin:]
        else:
            paragraph = self.doc[begin:end]

        if paragraph == self._get_sentence(doc[token_ref[0]:token_ref[1]].sent):
            raise DegenerateSelection
            
        return paragraph
    

    def _get_segment(self, token_ref, range_num=None):
        """
        Gets a segment of paragraphs around token_ref. range_num is number
        of paragraphs before and after that must be included in the lookup; default
        is a single paragraph before and after
        """
        if range_num is None:
            range_num = DocUtility.BASE_SEGMENT_DEF
            
        begin_reference = index.lookup(token_ref[0])
        end_reference = index.lookup(token_ref[1])
        start_par = begin_reference["paragraph"]
        end_par = end_reference["paragraph"]

        if start_par <= range_num:
            prior_start_par = 1
        else:
            prior_start_par = start_par - range_num
        final_par = index.get_number_of_paragraphs()
        if end_par >= final_par + 1 - range_num:
            next_end_par = final_par
        else:
            next_end_par = end_par + range_num

        if prior_start_par == next_end_par:
            raise DegenerateSelection
            
        # look up token offsets for current paragraph
        (begin, end) = self._get_paragraph_range(prior_start_par, next_end_par)
        if end is None:
            segment = doc[begin:]
        else:
            segment = doc[begin:end]

        if len(segment) <= len(self._get_segment(token_ref, DocUtility.BASE_SEGMENT_DEF)):
            raise DegenerateSelection
                                                       
        return segment


    def _get_segment_exp(self, token_ref):
        """bound shortcut for use in lambda. 3 paragraphs before and after"""
        return _get_segment(token_ref, DocUtility.EXP_SEGMENT_DEF)
        

    def _get_section(self, token_ref):
        begin_reference = self.index.lookup(token_ref[0])
        end_reference = self.index.lookup(token_ref[1])
        start_seq = begin_reference["section_seq"]
        end_seq = end_reference["section_seq"]
        # look up token offsets for current paragraph
        (begin, end) = self._get_paragraph_range(start_seq, end_seq)
        if end is None:
            section = self.doc[begin:]
        else:
            section = self.doc[begin:end]

        if len(section) <= len(self._get_segment(token_ref, DocUtility.EXP_SEGMENT_DEF)):
            raise DegenerateSelection
            
        return section

        
    def get_scoped_selection(self, token_ref, scope):
        """
        This gets a selection of text, given a token reference. The bigger
        the scope, the larger the token reference produced.
        :param token_ref - (begin, end) tuple of numerical offset of the selection
        at which the search string was found
        :param scope - one of the scope values above. The bigger the scope, the
        larger the selection
        :returns - string with selection. NOTE: presently, there is no highlighting
        of the matched string. In later versions, we will pass back formatted strings
        with highlighting of the mached values.
x>        """
        scope_lambdas = {
            DocUtility.SENTENCE: self._get_sentence,
            DocUtility.PARAGRAPH: self._get_paragraph,
            DocUtility.SEGMENT: self._get_segment,
            DocUtility.EXP_SEGMENT: self._get_segment_exp,
            DocUtility.SECTION: self._get_section
        }

        return scope_lambdas[scope](token_ref)


    def get_next_scoped_selection(self, token_ref, scope, ignore_length_warning):
        """
        This gets the next-higher selection of text, given the current scope.
        :param token_ref - (begin, end) tuple of numerical offset of the selection
        at which the search string was found
        :param scope - one of the scope values above. The bigger the scope, the
        larger the selection
        :param ignore_length_warning
        :returns - a tuple;
        [0] string with selection. NOTE: presently, there is no highlighting
        of the matched string. In later versions, we will pass back formatted strings
        with highlighting of the mached values.
        [1] the scope of the selection
        """
        next_scope = {
            DocUtility.SENTENCE: DocUtility.PARAGRAPH,
            DocUtility.PARAGRAPH: DocUtility.SEGMENT,
            DocUtility.SEGMENT: DocUtility.EXP_SEGMENT,
            DocUtility.EXP_SEGMENT: DocUtility.SECTION
        }

        try:
            if scope != DocUtility.SECTION:
                text = self.get_scoped_selection(token, next_scope[scope])
                return (text, next_scope[scope])

        except:
            pass

        # if reached here, you will have one of two options - either call at
        # next level or bail with exception
        if not ignore_length_warning:
            raise DegenerateSelection

        if scope == DocUtility.SECTION:
            # just return the whole darn thing
            text = self.doc[:]
            return (text, DocUtility.DOCUMENT)
        else:
            return self.get_next_scoped_selection(token_ref, next_scope[scope], True)
