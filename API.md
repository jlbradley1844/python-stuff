# SERVICE REST API

Goal of this is to provide a reasonable, extensible rest-style API for
performing search operations with the site. Naturally, the bulk
of these are going to be GET operations, since they will not change
the data. The first draft will consist entirely of GET operations. This will
NOT involve database storage, and should it later be needed, a simple ORM
against a simple SQL back end will be used.

PLEASE NOTE: _The engine itself should be coded
in such a way that it can be used in both web applications and standalone
programs (via compiled python). This API is what the Django code will work
with, but it should be a thin layer around the document search object, which
itself can be used on any platform. The main challenge with a standalone
engine is getting something compiled and freestanding that includes spacy and
whatever other libraries I want to pull in.

### GetCategories
This returns a list of "categories" under which the works to be searched
are sorted. This is a list of ASCII qualifiers. For Baha'i works, the
categories are authors; e.g. "Baha'u'llah, Abdul-Baha, UHJ." For other works
the categories are either religions themselves or large known works
representative of the religion; e.g. "Judaism", "Bible," etc. Returns as
{"categories"=[]}  where [] contains a JSON array of categories.

### GetDocumentTags
GetDocumentTags[/<Category>]
This gets the list of mnemonic tags. These mnemonic tags are unique
ASCII tags used to identify individual document works. If the Categories
path is specified, this gets the documents under which the categories
are filed.
{"tags"=[{"tag":<>,"category":<>}]}  where [] contains a JSON array of objects

### OpenSession
This returns a 256-bit ASCII hash. It will be used to tie searches from
one sequence to the next where this is needed. For those commands that
support sessions, the session will be supplied with the 'session='
argument. Sessions expire within 24 hours or when the service is
restarted. In lieu of authentication, sessions are tied to IPs. The same
IP will be unable to open more than 1000 sessions in a day, as a throttling
mechanism. That simpleminded strategy should avoid usage abuse. Returns
{"sessionid"=...}

### SimpleSearch
SimpleSearch?token.1=<>&token.2=<>&...,[documenttag.1=<>&documenttag.2=<>]
SimpleSearch[/<Category>]
SimpleSearch[/<DocumentTag>]
This performs a document search of one or more tokens. Each token will be
a lemma match in spacy. If more than one token is supplied, it is presumed that
ALL tokens must be present in the order given, with possible words intervening
in that sentence. This is conjunctive. It will return a JSON object with the
following fields:
DocumentTag: document tag
DocumentMetadata: document metadata as supplied in configuration file
Selection: sentence within which a the document is supplied
SelectionScope: will always return "Sent" for sentence. 
SelectionSession: session used to perform subsequent operations on the selection.

### ExpandSelection
ExpandSelection?session=<>&scope=<>
This does an "exand" of the selection based on the current scope that was
given to the user. It will the return a JSON object indicating
Selection: expanded selection
SelectionScope: the current scope of selection
IsComplete (optional): if "yes", then this is the complete document, and no further
calls to ExpandSelection will have an effect.
The selection scope values are as follows
"sent" - sentence-level. Lowest scope
"para" - gets entire paragraph
"segment" - gets paragraph before and after
"expseg" - gets three paragraphs before and after. Is not returned if this contains
an entire section.
"sect" - gets either an entire section from the writings if it is
less than or equal to 50 paragraphs.
This should always return the next-bigger selection. In case of degenerate
values it should return the next-bigger selection; e.g. if you have a sentence and
the "para" scope returns the same thing because the paragraph is only a sentence,
the "segment" scope should be returned instead.
There is one possible error returned instead of JSON
"error" - "EXPAND_CALL_TOO_BIG"
"userMessage" - will be one of these messages
   "Do you wish to get the whole section? It is %n paragraphs long."
   "Do you wish to get the whole document? It is %n paragraphs long."
The UserMessage is suitable for end-user display.

### ExpandSelectionOverride
ExpandSelectionOverride?session=<>&scope=<>
This is called when a user wishes to expand a section when the current
selection is "Section," or if the current selection is "SegmentExp" but
the selection is over 10000 characters). It will return the same values as
the ExpandSelection call.


# HIGH LEVEL DESIGN
Initially no database will be used. There will be one object DocumentEngine
into which all object calls will take place. This is the object which manages
access to the Spacy documents and metadata.

It will contain a reference to the high-level document search object, and
several management objects:
* SessionMap
   - DocumentReference
   - Index
   - ClientIP
