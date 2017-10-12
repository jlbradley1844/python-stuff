This is a repository for the Baha'i writings. These are from the text sources
in Gutenberg. You can get more by using wget; e.g.

wget http://www.gutenberg.org/files/16940/16940-0.txt

will get the file and store under that name in the current directory (that
particular link is for Gleanings).

To get the Natural Language Toolkit:
sudo apt install python-pip
sudo pip install -U nltk
sudo pip install -U numpy

To get SpaCy, with the default English module:
sudo pip install -U spacy
sudo python -m spacy download en
(after this, you can load the model, like so:

import spacy
nlp = spacy.load('en')
doc = nlp(textInputObject)

=============================

# CHALLENGES IN NATURAL LANGUAGE PROCESSING FOR THE BAHA'I WRITINGS

A common problem is the need to index and correlate the Baha'i
writings. This is necessary due to the "text-based" nature of the
Baha'i Faith.

This places it in some very limited company, perhaps only on part with
certain sects of Judaism and Hinduism. Most religions take one of two
attitudes toward their holy texts:

1. There is no established corpus. While there are some writings that
are said to be central, and while some believers may treat specific
writings as essentially infallible, this is not applicable to all
believers. There may be an enormous amount of text, much of it
commentary. As such, textual analysis is important for the study of
that faith, but is not so central as to be critical, and other
authority figures may have more say. Buddhism,
Hinduism and many religions of the orient fall into this category, but
to some extent Roman Catholicism and other "high Protestent"
denominations do as well.

2. There is an established canon. The writings are said to be
infallible; where acknowledged authority figures do exist, they tend
to base much of their authority on deep familiarity of the religious
canon. In such cases, the canon is fixed and generally of manageable
size.  For instance, many Christians regard the Bible as the entire
canon word, and regard nothing else is authoratative.  Likewise, in
Islam one has the Koran and a handful of Hadith that are regarded as
canon, particular sects regarding only particular Hadith as
qualifying; in conservative Judaism it may be the Pentateuch and
certain parts of the Midrash, and so on.

3. Then there is the category of an established canon of nearly
overwhelming size.

The Baha'i Faith is in this unusual third category, where a very large
corpus exists, much of it is regarded as infallible, and all of it
tends to be regarded as essential. The corpus is essentially, all
writings of the three central figures; additionally, particular
authority is assigned to writings of The Guardian and the Universal
House of Justice. All have produced an enormous corpus. Even limiting
oneself to the authorized translations, which are acknowledge to be
only ten to twenty percent of the writings, there is more than the
strictured canon of other religions that recognize one. Finally,
Baha'is also regard the central texts of other religions (particularly
the Koran and the Bible) as being divinely inspired, if not
infallible.

This makes it particularly necessary to produce tools for study of the
Baha'i Writings to help cope with the depth of the writings. To this
point, tools have been helpful, but limited to the simplest
"token-matching" algorithms. For example, the _Ocean_ toolkit, which
is highly recommended, seems to do exact string matches. This fills an
important need, but is not at the level of the sophisticated
concordances available to many Christians.

Hence the need for some sort of more sophisticated lexical analysis of
the writings. Open-source natural language processing tools have
become good enough to allow sophisticated analysis without spending
weeks in software development to perform simple tasks. The writings
themselves have particular challenges. Fortunately, there are certain
things that are characteristic of the writings that make analysis
easier than many NLP tasks.

## Challenges of The Writings

This section will confine itself to particular characteristics of the
central texts, as they have been made available for textual
analysis. Other religious texts, while central to The Faith, have
different challenges, and must be regarded on their own.

There is also the problem that all of these writings, save certain
writings of Shoghi Effendi, exist in English only in translated
versions. Textual analsyis therefore takes place one step removed from
the actual text. For Baha'is, this is generally not regarded as much
of a concern, as the texts in English are regarded to some extent as
being "interpretive" and worthy of their own study as such. However,
it should be mentioned.

1. Specialized, Particular Terminology

The Baha'i Writings tend to use particular poetic words and phrases to mean
something else entirely. For instance, "Blessed Beauty" or "The Pen of
the Most Glorious" to mean Baha'u'llah. The writings are full of these
phrases, and any concordance must recognize these phrases and treat
them as effectively being synonyms of one another. Likewise, many of
Abdu'l-Baha's writings use language used by classical philosophers
such as Aristotle, for which current English usage assigns different words.

2. Occasional Archaic Language, including Pronouns

Shoghi Effendi chose to use the English of the King James Bible to
elevate the translated text. In particular, he uses the pronouns
"Thee" and "Thou," and verb conjugates related to those pronouns
("art" instead of "are") throughout the writings. Unfortunately, these
are not part of modern English usage. This will require updating the
internal models to ensure that "Thee" is treated as "you" and
associated with the reader or that spoken to accordingly.

3. Preformatted Text Sources

As far as I know there is no "raw" text repository of the
writings. Rather, the closest thing that is publicly available is the
text file repository at Gutenberg. This is both complete and requires
a minimum of preprocessing. However, it does require some
preprocessing. Front matter, appendexes and headers must be stripped
off. Ideally, the text should be split into sections and/or paragraphs
to allow this sort of labeling to take place. These sections should
also be properly cross-referenced with the sources (see next point).

4. Need to trace sources

When producing program output, it is necessary to produce accurate
source citations. This is something a lot of NLP programs don't have
to deal with. In many cases, some sort of standardization already
exists; e.g. section and chapter numbering, or for many newer
editions, standard paragraph markings are used. However, for many
older works that have not had newer editions, they only citation
method available is page numbers. This can lead to problems in
excerpting text, since those do not break cleanly along paragraphs,
but happen in the middle of sentences.

5. Handling of Internationalized Character Sets

Shoghi Effendi standardized on a particular set of diacriticals. He
settled on this long before the current standardized diacriticals for
Arabic and Persian now in use. For the purposes of textual analysis,
the main challenge is to retain the diacriticals whenever
possible. Many NLP processors attempt to simplify things by forcing
text to ASCII. Fortunately, most parsers nowadays are
Unicode-aware, allowing such things to be retained. However, when
doing analysis, user input itself probably will not have the
diacritical. So for instance, a search for "Baha'u'llah" should return
all references even though it has no diacriticals.

6. Handling of Quotations

Quotations can always be tricky, but they are important to associate
with speakers. These are particularly important in two areas. The
writings of Shoghi Effendi are full of lengthy quotes from Baha'u'llah
and Abdu'l-Baha, and in processing, it is important to recognize the
speaker as being them, rather than Shoghi Effendi. This is
particularly important because there are a few cases where this is the
only source of translated material; additionally, Shoghi Effendi
rarely gave citations of the works he quoted, making it desireable to
cross-reference against other translations (a task made easier by the
fact that translators tendend to keep Shoghi Effendi's translated
passages intact when later translating the larger work from which it
came). The other case is when Baha'u'llah or Abdu'l-Baha quote from
clerics or other critics, to answer or even mock such critics - we
obviously do not want to include this in our analysis since they are
frequently the opposite of what The Faith teaches! Contrast this to
the situation in the Gospels, where the quotations of Jesus Christ may
be the most important part of the corpus.


## Helpful Characteristics of The Writings

1. Fixed, "Small" Corpus Size

On the other hand, the corpus is small and static. With respect to
what, one might ask? In this case, it is with respect to language
analysis tools Many NLP programs are written to deal with enormous
amount of texts; projects like Apache Solar may deal with millions of
documents without difficulty. Contrast this with the Baha'i writings:
as extensive as they are, they can easily fit in the RAM of even the
most modest-sized computer. This means that general-purpose NLP
analyzers can be used on the entire corpus at once, something that
would've been unthinkable when the first serious programs for the
Baha'i Writings came out.

2. Formalized Language and Synonyms

The use of fixed metaphors is actually an advantage to textual
analysis. While much abstract language is imprecise, the varied idioms
in the writings are generally very precise in their meaning. As such,
one can identify these idioms, define synonyms with them, and
generally use them meaningfully in analysis. The fact that Shoghi
Effendi tended to use the same idioms and the translators that came
after him use the same ones help the situation immensely. Were this
not the case, we would have trouble correlating related ideas in the
writings that would be evident from examining the untranslated text.

With that in mind, there are a number of techniques we have to use in
our analysis.

## A General NLP "Pipeline"

Natural Language Processors are often thought of as a pipeline. The
idea is that you start at the highest level, and each stage breaks
down a piece of text into meaningful parts. For instance, let's think
of a piece of work like _Gleanings from the Writings of Baha'u'llah_.
The pipeline might go something like this:

1. Pull in the raw text

2. Strip off the front matter, table of contents, etc.; eliminate any
other extraneous matter such as page headers.

3. Separate out each of the numbered sections. Each section will be
analyzed independently.

4. Break the section into sentences.

5. Break the section into individual words ("tokens").

6. Identify the parts of speech in each sentences.

7. Identify the "entities" in the corpus.

For much of the history of computing, this sort of deterministic
chunking is how things got done. Early results were promising but
ultimately unsuccessful, in part due to the strict nature of these
pipelines. For instance, to identify sentences, you had to tell if a
period was because the sentence was over, if it was in a quotation or
if it was due to an abbreviation; to do that you had to be able to
tell what part of speech the period followed, which required
identifying the sentence.

The field advanced greatly since the late eighties, partly due to
increased computational power, but also due to new artificial
intelligence techniques that used probabalistic models to assist with
the process. Tools nowadays like *spaCy* and *nltk* allow one to
perform complext text analysis without programming any of the
constituent parts of the pipeline. For instance, this snippet of code
in spaCy will read text and then perform the pipeline:

``` python
# read in the text file you wish to analyze
with open('gleanings.txt', 'r') as myfile:
    text=myfile.read()
# set up spacy
import spacy
nlp = spacy.load('en')    # use English
# initialize the pipeline
# the Gutenberg text downloads are already in utf8, following is for python2
utext=unicode(text.decode('utf8'))
doc = nlp.tokenizer(utext)
# perform the pipeline processing
nlp.tagger(doc)
nlp.parser(doc)
nlp.entity(doc)
```

That is essentially it. The pipeline initialization also does
tokenization (step #5), the tagger identifies parts of speech (step
#6), the parser pulls apart the sections (steps 2-4), and the last
instruction performs entity identification (step #7). Note that the
pipeline is now in a different order, to better allow newer
statistical methods to be used for improved accuracy.

Once you have it loaded, you can do a few things with it.

## Some Scenarios for Analysis

### Naive Search

String-based text search can be used in text, and is still "good
enough" in many cases. But by simply using NLP tools, we can do a
little better quickly - you don't need to worry about placement of
whitespace, punctuation or anything. One word, multiple words in a
sentence, multiple words in the same secion - you can do that.

Doing a straight search in the document is insufficient, as you want
to see the search results within the context of the passage within
which it is found. The algorithm for doing so might look something
like this:
a. Break the document into various subdocuments
b. Find those subdocuments that actually "pass" the match
c. Display the subdocuments
d. Highlight the areas of the subdocuments that match

### Entity Search

Once you get past this point, you can search for both the words and
the synonyms for the words. The same general search algorithm from
above works in this case as well.


### Adding References



## Some Miscellaneous Problems and How to Handle Them

### Saving Your State
Once you preprocess your document, you can save it out to disk and
fetch it later:
Doc.to_disk()
Doc.from_disk()

Something like this would be useful for an IPython-type setup within
which one could work with individual documents or document collections.

### Pulling from document one sentence at a time
Doc.sents - returns an iterator over the sentences in the
document. Each sentence is held in a Span object.


### Search operations


Search operations return a Span object. You can use the Span's lefts
and rights objects to return tokens to the left and right of the
span. A rough algorithm might look something like this:

-> Set up a search to iterate over documents+paragraphs/sections
-> "Push" the document name
-> Get the next "paragraph" (marked by two line-feeds in a row)
-> Examine paragraph for header match. If it matches header (e.g.,
single sentence, all-caps), push the header
Else
-> increment the paragraph number and search the section.
If it is a text paragraph:
-> search for the entry
If entry is found:
-> "highlight" the entry in the paragraph (there may be multiple) and
containing sentence (maybe)
-> pop the document name and paragraph, then push the <document,
paragraph_no, formatted_text> tuple to the "found" collection

This routine would return a collection that could then be formatted a
number of different ways.

N.B. I don't understand the search yet... need to figure how to
integrate the callback, or whateveritis.

### Entity-matching


