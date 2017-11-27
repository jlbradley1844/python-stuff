from docmetadata import DOCUMENT_INDEX, CATEGORIES
from documentcollection import DocumentCollection
from docutility import DocUtility

class DocumentEngine:
    """
    The "engine" in the search framework. This is a management object
    that is used to dispatch searches and retrieve document information
    from those searches.
    """

    
    def __init__():
        """
        sets up the management objects
        """
        self.doc_collection = DocumentCollection()
        self.session_track = {}


    def get_categories():
        """
        Returns the category metadata array
        """
        return CATEGORIES


    def get_document_tags(self, category=None):
        """
        Returns an array of tags, associated with the category each is
        associated with
        :param optional. If supplied, returns only those tags that match the category
        """
        if category is None:
            tag_coll = [{
                "tag": key,
                "category": DOCUMENT_INDEX[key]["category"]
            } for key in DOCUMENT_INDEX]
        else:
            tag_coll = [{
                "tag": key,
                "category": category
            } for key in DOCUMENT_INDEX
                where DOCUMENT_INDEX[key]["category"] = category]
                        
        return tag_coll


    def get_metadata(self, tag):
        """
        Returns the document metadata associated with a tag. Returns the
        hardcoded lookup values from DOC_METADATA
        """
        return DOC_METADATA[tag]
    

    def simple_search(self, tokens, document_tags=None, category=None):
        """
        Returns a document and a reference inside the document with
        those matches.
        :param tokens: array of tokens to match. N.B. inital implemenation
        to be just ONE SINGLE WORD. ADDITIONAL TOKENS WILL BE IGNORED.
        :param documen_ttags: optional. If specified, indicates the set of
        documents the search is applied to. If not specified, matches all.
        :param category: optional. If specified, indicates the category of
        documents the search is applied to. Only used if documenttags=None
        :returns array of json-style objects; each object consisting of
        "tag" - which document it was found in
        "selection" - sentence within which the token(s) found
        "scope" - the scope of selection, which is always "sent"
        "section" - section of document
        "para" - paragraph number
        """
        match_token = tokens[0]
        if category is not None and document_tags is None:
            document_tags = [key for key in DOCUMENT_INDEX
                             where DOCUMENT_INDEX[key]["category"] == category]

        raw_results = doc_collection.simple_search(match_token, document_tags)
        results = []
        
        # return array of text references, consisting of tag, sentence and scope
        for doc_tag in raw_results:
            doc = self.doc_collection.extract_doc[doc_tag]["nlpdoc"]
            index = self.doc_collection.extract_doc[doc_tag]["index"]
            for ref in raw_results[doc_tag]:
                found_ref = {}
                found_ref["tag"] = doc_tag
                begin = raw_results[ref][2]
                end = raw_results[ref][3]
                found_ref["selection"] = doc[begin:end].sent
                found_ref["scope"] = SCOPE.SENTENCE
                lookup_info = index.lookup(begin)
                found_ref["section"] = lookup_info["section"]
                found_ref["para"] = lookup_info["para"]

                results.append(found_ref)

        return results


    def expand_selection(self, tag, token_ref, current_scope, is_override=False):
        """
        Given a document tag and a reference into it, get the text associated
        with the next-bigger scope and returns the next bigger scope.
        - If the next-bigger scope is identical, increase the current_scope until
        you get something different
        - If the value to be returned is greater than MAX_SELECTION_SIZE tokens
        and is_override is false, then instead of returning something, an error
        object will be returned indicating that the expand cannot be made because
        it is too big. (In practice, this is used to prompt the user whether they
        really want that much document text.)
        :param tag - document tag
        :param token_ref - numerical index into document
        :param current_scope - SCOPE value indicating scope of text selection that has already
        been returned to the client.
        :param is_override - if false, will return error if section is above
        MAX_SECTION_SIZE. If true, will ignore warning and return as much text
        as is requested.
        :returns - dictionary object indicating the following
        "tag" - tag of document
        "token_ref" - token_ref passed in
        "selection" - text of new selection
        "scope" - scope of new selection passed back
        """
        doc = self.doc_collection.extract_doc[tag]["nlpdoc"]
        index = self.doc_collection.extract_doc[tag]["index"]
        doc_selector = DocUtility(doc, index)
        (text, scope) = doc_selector.get_next_scoped_selection(token_ref,
                                                               current_scope, is_override)
        return { "tag": tag,
                 "token_ref": token_ref,
                 "selection": text,
                 "scope": scope
                 }

