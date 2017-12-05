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


    def __init__(self, index, raw_string):
        """
        :param index - DocumentIndex object describing doc
        :param raw_string - original unicode string representation of spacy document
        """
        self.index = index
        self.raw_string = raw_string


    def _get_sentence(self, span):
        """
        Get the sentence a given token reference offset is in
        :param span - span containing found token
        :returns the sentence of text cotaining the span at the offset
        """
        return unicode(span.sent)


    def _get_paragraph_range(self, start_para, end_para = None):
        """
        Get the character offset range bounding one or more paragraphs in a range from the document
        :param start_para - Starting paragraph number to retrieve
        :param end_para - ending paragraph number.
        :returns tuple for (begin, end) character offsets. If end=None, then this means
        all text from begin and beyond should be fetched.
        """
        begin = self.index.get_paragraph_span(start_para)[0]
        end = self.index.get_paragraph_span(end_para)[1]
        return (begin, end)
        
        
    def _get_paragraph(self, span):
        begin_reference = self.index.lookup(span.start_char)
        end_reference = self.index.lookup(span.end_char)
        start_par = begin_reference["paragraph"]
        end_par = end_reference["paragraph"]
        # look up character offsets for current paragraph
        (begin, end) = self._get_paragraph_range(start_par, end_par)
        if end is None:
            paragraph = self.raw_string[begin:]
        else:
            paragraph = self.raw_string[begin:end]

        if len(paragraph) <= len(unicode(span.sent)):
            raise DegenerateSelection
            
        return paragraph
    

    def _get_segment(self, span, range_num=None):
        """
        Gets a segment of paragraphs around span. range_num is number
        of paragraphs before and after that must be included in the lookup; default
        is a single paragraph before and after
        """
        if range_num is None:
            range_num = DocUtility.BASE_SEGMENT_DEF
            
        begin_reference = self.index.lookup(span.start_char)
        end_reference = self.index.lookup(span.end_char)
        start_par = begin_reference["paragraph"]
        end_par = end_reference["paragraph"]

        if start_par <= range_num:
            prior_start_par = 1
        else:
            prior_start_par = start_par - range_num
        final_par = self.index.get_number_of_paragraphs()
        if end_par >= final_par + 1 - range_num:
            next_end_par = final_par
        else:
            next_end_par = end_par + range_num

        if prior_start_par == next_end_par:
            raise DegenerateSelection

        if (range_num > 1 and
            prior_start_par == start_par - DocUtility.BASE_SEGMENT_DEF and
            next_end_par == start_par + DocUtility.BASE_SEGMENT_DEV):
            raise DegenerateSelection
            
        # look up character offsets for current paragraph
        (begin, end) = self._get_paragraph_range(prior_start_par, next_end_par)
        if end is None:
            segment = self.raw_string[begin:]
        else:
            segment = self.raw_string[begin:end]

        return segment


    def _get_segment_exp(self, span):
        """bound shortcut for use in lambda. 3 paragraphs before and after"""
        return self._get_segment(span, DocUtility.EXP_SEGMENT_DEF)
        

    def _get_section(self, span):
        begin_reference = self.index.lookup(span.start_char)
        end_reference = self.index.lookup(span.end_char)
        start_seq = begin_reference["section_seq"]
        end_seq = end_reference["section_seq"]
        # look up character offsets for current paragraph
        (begin, end) = self._get_paragraph_range(start_seq, end_seq)
        if end is None:
            section = self.raw_string[begin:]
        else:
            section = self.raw_string[begin:end]

        if len(section) <= len(self._get_segment(span, DocUtility.EXP_SEGMENT_DEF)):
            raise DegenerateSelection
            
        return section

        
    def get_scoped_selection(self, span, scope):
        """
        This gets a selection of text, given a spacy Span object. The bigger
        the scope, the larger the string around the token
        :param span - spacy span of the selection at which the search string was found
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

        return scope_lambdas[scope](span)


    def get_next_scoped_selection(self, span, scope, ignore_length_warning=False):
        """
        This gets the next-higher selection of text, given the current scope.
        :param span - spacy span of the selection at which the search string was found
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
                text = self.get_scoped_selection(span, next_scope[scope])
                return (text, next_scope[scope])

        except:
            pass

        # if reached here, you will have one of two options - either call at
        # next level or bail with exception
        if not ignore_length_warning:
            raise DegenerateSelection

        if scope == DocUtility.SECTION:
            # just return the whole darn thing
            text = self.raw_string
            return (text, DocUtility.DOCUMENT)
        else:
            return self.get_next_scoped_selection(span, next_scope[scope], True)


    def clean_whitespace(self, str):
        """utility to remove line feeds"""
        # common python idiom - split splits on ANY whitespace, and join joins
        # using it
        return " ".join(str.split())
