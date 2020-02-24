import re

class WordCount:
    """Count words in a submitted text."""

    def count(self, text):
        """Return the number of words in the submitted text."""

        if text == '':
            return 0

        words = text.split()

        return len(words)

class SyllableCount():
    """Count the number of syllables in a string of words.

    The number of syllables in a word is needed for the Flesch Reading Ease
    test and the Flesch-Kincaid Grade Level test.

    The algorithm counts vowels and assumes one syllable per vowel. It takes some of
    the exceptions to this rule into account. Runs of multiple adjacent vowels are counted
    as a single vowel. Special situations such as words that end in 'ale', 'ige'
    and the like are accounted for. A few outlier words that don't amend themselves
    to rule-based counting are accounted for ('segue' and 'toque' for example). The
    letter 'y' is counted as a vowel unless it's the first letter of a word.
    """

    def count_syllables(self, text):
        """ Return the number of syllables in a word."""

        words = text.split()
        syllables = 0

        for word in words:
            syllables += self._count_syllables_in_word(word)

        return syllables

    def _advance(self):

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def _count_syllables_in_word(self, word):

        # Need to remove trailing punctuation so that the outlier words can be detected
        word = re.sub(r'^(\w+)[\.\?:;,!]',r'\1',word)

        self.text = word.lower()
        vowel_count = self.pos = 0
        self.current_char = self.text[self.pos]
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']

        if self.current_char == 'y':  # skip Y if it's the first letter. ie, not a vowel
            self.pos += 1

        # outliers
        if self.text in ['toque', 'rogue', 'vogue']:
            return 1

        if self.text in ['marque', 'subdue', 'cafe', 'ok', 'shuddered', 'murdered']:
            return 2

        if self.text in ['finale', 'avenue']:
            return 3

        if self.text in ['reality', 'minutiae']:
            return 4

        # for words that end in 'ue'
        if len(self.text) >= 6 and self.text[-2:] == 'ue':
            vowel_count = -1

        # for words that end in 'ale', 'ige', and the like
        if len(self.text) >= 3 and self.text[-1] == 'e' and self.text[-3] in vowels:
            vowel_count = -1

        while self.current_char is not None:

            while self.current_char is not None and self.current_char not in vowels:
                self._advance()

            while self.current_char is not None and self.current_char in vowels:
                vowel_count += 1
                # consume runs of vowels (ie dipthongs, etc)
                while self.current_char is not None and self.current_char in vowels:
                    self._advance()

                self._advance()

        return vowel_count

class SentenceCount:
    """Count sentences in submitted text."""

    def count_sentences(self, text):
        """Returns the number of sentences in text or zero if text is empty."""

        if text == '':
            return 0

        text = re.sub('[”\'"]','',text) # '.” ' doesn't match the re, so remove the quotes

        return len(re.split('[\.!:\?]\s', text))

    def split_into_sentences(self, text):
        """Returns a list of sentences in the text.

        Unfortunately does not include the sentence's ending punctuation.
        """

        text = re.sub('[”\'"]','',text) # '.” ' doesn't match the re, so remove the quotes

        return re.split('[\.!:\?]\s', text)

class Readability():
    """Provides methods for various readability scores.

    Supported scores:
        * Flesch-Kincaid Grade Level
        * Flesch Reading Ease

    Supported properties:
        * total_words
        * total_sentences
        * total_syllables
    """

    def _get_counts(self, text):

        wc = WordCount()
        self.total_words = wc.count(text)
        sc = SentenceCount()
        self.total_sentences = sc.count_sentences(text)
        sy = SyllableCount()
        self.total_syllables = sy.count_syllables(text)


    def flesch_reading_ease(self, text):
        """Returns the value or zero if text is empty."""

        text = text.rstrip()
        self._get_counts(text)

        try:
            self.words_per_sentence = self.total_words/self.total_sentences
            self.syllables_per_word = self.total_syllables/self.total_words
            score = 206.835 - (1.015*self.words_per_sentence) - (84.6*self.syllables_per_word)
        except ZeroDivisionError: # generally happens when text == ''
            self.syllables_per_word = 0
            self.words_per_sentence = 0
            return 0

        return score

    def flesch_kincaid_grade_level(self, text):
        """Returns the grade level or zero if the text is empty."""

        text = text.rstrip()
        self._get_counts(text)

        try:
            self.words_per_sentence = self.total_words/self.total_sentences
            self.syllables_per_word = self.total_syllables/self.total_words
            score = (.39*self.words_per_sentence) + (11.8*self.syllables_per_word) - 15.59
        except ZeroDivisionError: # generally happens when text == ''
            self.syllables_per_word = 0
            self.words_per_sentence = 0
            return 0
        return score

class SpellCheck:
    """Provides spell checker services.

    By default, the list of words is stored in a file called 'spell'
    in the current working directory. You can specify a different
    filename when creating a SpellCheck object. If the file can't be
    opened for any reason, an exception is raised and the object is
    not created.

    check_spelling(text)
        Returns a dict in the form {"word1":n, "word2":n, ...} where
        n is the position of the misspelled word in the text.

    add_word(word)
        Adds a single word to the filename that's specified when
        you instantiate the object.
    """

    filename = ''
    word_list = set()

    def __init__(self, filename='spell'):
        word_list = self.word_list
        self.filename = filename # for use in the add_word() method
        try:
            with open(filename, 'r', encoding='utf8') as spellcheck:
                for word in spellcheck:
                    word_list.add(word.strip()) # strip off the trailing '\n' character
        except Exception:
            raise

    def add_word(self, word):
        """ Adds a word to the end of the spell check file"""

        filename = self.filename
        if word not in self.word_list:
            with open(filename, 'a') as f:
                print(word, file=f)

    def check_spelling(self, text):
        """Spell checks the submitted text. Returns a dict
        where the key is the misspelled word and the value is
        the word number in the text.
        """

        input_text = set()
        word_list = self.word_list
        misspellings = {}

        for word in text.split():
            input_text.add(word.strip('<>.,:;"\'(){}[]!?'))

        bad_spelling = input_text - word_list

        x = 1
        for w in text.split():
            word = w.strip('<>.,:;"\'(){}[]!?')
            if word in bad_spelling:
                misspellings[word] = x
            x += 1

        return misspellings


####################################
# End of class defs. Start of tests.
####################################

def test():

    text = "We live in strange times. All evidencer shows we’re driving ourselves to a climate breakdown that threatens our survival, and what do governments do? Do they employ the many available solutions and work to educate the public and resolve the crisis? A few are trying, while some outright deny the evidence, some attack citizens who speak out about the emergency and others claim to care while planning ways to sell enough fossil fuels to cook the planet." # Source: David Suzuki

    sc = SpellCheck()
    print(sc.check_spelling(text))
    #sc.add_word('strange')
    #sc.add_word('Do')
    #sc.add_word('governments')
    #newsc = SpellCheck('spell-test')
    #print(newsc.check_spelling(text))

    wc = WordCount()
    test_pass = test_word_count(wc)

    sc = SentenceCount()
    test_pass = test_sentence_count(sc)

    sy = SyllableCount()
    test_pass = test_syllable_count(sy)

    readability = Readability()
    print('Flesch-Kincaid grade: {:.2f}'.format(readability.flesch_kincaid_grade_level(text)))
    print('Flesch readability ease: {:.2f}'.format(readability.flesch_reading_ease(text)))
    print('Total words: {}'.format(readability.total_words))
    print('Total sentences: {}'.format(readability.total_sentences))
    print('Total syllables: {}'.format(readability.total_syllables))
    print('Average words/sentence: {:.2f}'.format(readability.words_per_sentence))
    print('Average syllables/word: {:.2f}'.format(readability.syllables_per_word))

    return test_pass

def test_sentence_count(sc):

    test_pass = True

    paragraphs = [
        ('The Golub Syntactic Density Score was developed by Lester Golub in 1974?" It is among a smaller subset of readability formulas that concentrate on the syntactic features of a text: To calculate the reading level of a text, a sample of several hundred words is taken from the text. The number of words in the sample is counted, as are the number of T-units. A T-unit is defined as an independent clause and any dependent clauses attached to it. Other syntactical units are then counted and entered into the following table', 6)
    ]

    for item in paragraphs:
        count = sc.count_sentences(item[0])
        if count != item[1]:
            print('Bad sentence count: "{}..."'.format(item[0][:10]))
            print(' -> Got {} sentences but expected {}'.format(sc.count_sentences(item[0]), item[1]))
            test_pass = False

    return test_pass

def test_word_count(wc):

    test_pass = True
    word_count_test_list = [
        ('hi there you people ', 4),
        ('http://example.com/etc is a web site', 5),
        (' http://example.com/etc is a web site ', 5),
        (' There are not 234 words in this sentence. ', 8)
    ]
    for item in word_count_test_list:
        if item[1] != wc.count(item[0]):
            print('Bad count: "{}"'.format(item[0]))
            print(' -> Got {} words but expected {}'.format(wc.count(item[0]), item[1]))
            test_pass = False

    return test_pass

def test_syllable_count(sy):

    test_pass = True

    syllable_count_test_list = [
        ('hello', 2), ('mountain', 2), ('syllable', 3), ('Apple', 2),
        ('your', 1), ('yellow', 2), ('invisible', 4), ('hyphenation', 4),
        ('triceratops', 4), ('popsicle', 3), ('pane', 1), ('finale', 3),
        ('see', 1), ('increase', 2), ('the', 1), ('he', 1), ('I', 1), ('concentrate', 3),
        ('people', 2), ('service', 2), ('colleague', 2), ('value', 2),
        ('average', 3), ('technique', 2), ('argue', 2), ('toque', 1), ('glue', 1),
        ('avenue', 3), ('marque', 2), ('mosque',1), ('subdue', 2), ('plague', 1), ('unique', 2),
        ('readability', 5), ('reality', 4), ('cafe',2)
    ]
    for item in syllable_count_test_list:
        count = sy.count_syllables(item[0])
        if count != item[1]:
            print('Bad count: "{}"'.format(item[0]))
            print(' -> Got {} syllables but expected {}'.format(count, item[1]))
            test_pass = False

    return test_pass

if __name__ == "__main__":
    test()

