# -*- coding: utf-8 -*-
import os
import nltk
import string
from file_util.macros import load_general

#The directory of the current module
dir_path = os.path.dirname(os.path.abspath(__file__))
tnt = load_general("{}/trigram_hmm.pkl".format(dir_path))
sno = nltk.stem.SnowballStemmer('english')
bad_np_word = [
    "i.e.", "i.e", "i.e.,",
    "e.g.", "e.g", "e.g.,",
    "is", "are",
    "was", "were",
    "when", "what", "then", "whenever"
]


def stemmer(wrd=''):
    return sno.stem(wrd)


def get_puntuations():
    '''Some basic puntuations'''
    puntuations = set(string.punctuation)
    return puntuations


def get_np_idx_list(np_list=None, tagged_token_list=None):
    """
    Return the list of syntactic pattern
    :param dec: declaration string
    :param tup_list: list of tuples
    :return: list of POS tags
    """
    if np_list is not None and tagged_token_list is not None:
        token_list = [tt[0] for tt in tagged_token_list]
        for idx in (i for i, token in enumerate(token_list) if token == np_list[0]):
            if token_list[idx:idx+len(np_list)] == np_list:
                return [idx, idx+len(np_list)-1]
    return None


def leaves(tree):
    """
    Finds NP (nounphrase) leaf nodes of a chunk tree.
    """
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()


def acceptable_word(word):
    """
    Checks conditions for acceptable word: length, stopword.
    We can increase the length if we want to consider large phrase
    """
    accepted = bool(len(word) <= 40 and word)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [w for w, t in leaf if acceptable_word(w)]
        yield term


def parse_np_range_list(tokens=None):
    """
    Refer to https://www.nltk.org/book/ch07.html
    :param texts:
    :return:
    """
    np_range_list = []
    # Nouns and {Adjectives, Adverbs}, terminated with Nouns

    grammar = r"""
                 NBAR:
                 {<DT>?<RB.*|JJ.*|VB.*|NN.*>*<NN.*>}  # Nouns and {Adjectives, Adverbs, Verbs}, terminated with Nouns

                 NP:
                 {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
                 {<NBAR>}
               """

    chunker = nltk.RegexpParser(grammar)
    # print chunker

    puntuations = set(string.punctuation)

    # POS Tag
    if not tokens:
        pass
    elif type(tokens) is list and type(tokens[0]) is tuple:
        # DEC Extraction
        tree = chunker.parse(tokens)
        terms = get_terms(tree)
        for term in terms:
            tmp = []
            for word in term:
                if word in puntuations:
                    pass
                elif word.replace(' ', '') == '':
                    pass
                elif word in bad_np_word:
                    pass
                else:
                    tmp.append(word)
            #print "tmp: ", tmp
            if tmp:
                np_range = get_np_idx_list(tmp, tokens)
                if np_range is not None:
                    np_range_list.append(np_range)
    else:
        print "Please input the text with its post tag in list of tuples..."
    return np_range_list


def parse_np_range_list_0(tagged_token_list=None):
    """
    Refer to https://www.nltk.org/book/ch07.html
    :param texts:
    :return:
    """
    np_range_list = []
    # Nouns and {Adjectives, Adverbs}, terminated with Nouns
    grammar = r"""
                 NP:
                 {<DT>?<RB.*|VB.*|JJ.*|NN.*>*<NN.*>}
               """

    chunker = nltk.RegexpParser(grammar)
    puntuations = set(string.punctuation)
    if type(tagged_token_list) is list and type(tagged_token_list[0]) is tuple:
        # DEC Extraction
        tree = chunker.parse(tagged_token_list)
        terms = get_terms(tree)
        for term in terms:
            #print "term: ", term
            np_list = []
            for word in term:
                if word in puntuations:
                    pass
                elif word.replace(' ', '') == '':
                    pass
                elif word in bad_np_word:
                    pass
                else:
                    np_list.append(word)
            if np_list:
                np_range = get_np_idx_list(np_list, tagged_token_list)
                if np_range is not None:
                    np_range_list.append(np_range)
        print "np_list: ", np_list
        print "np_range_list: ", np_range_list
    else:
        print "Please input the text with its post tag in list of tuples..."
    return np_range_list


def pos_correction(tagged_token_list=[]):
    """
    Correcting POS tags predicted by NLTK model into standard ones
    :param token_list: list of tuples for each token (word or ME)
    :return:
    """
    #correct_tagged_list = []

    for i in range(len(tagged_token_list)):
        if tagged_token_list[i][0] == '(':
            tagged_token_list[i] = (tagged_token_list[i][0], '-LRB-')
            #correct_tagged_list.append((tagged_token[0], '-LRB-'))
        elif tagged_token_list[i][0] == ')':
            tagged_token_list[i] = (tagged_token_list[i][0], '-RRB-')
            #correct_tagged_list.append((tagged_token[0], '-RRB-'))
        else:
            pass
            #correct_tagged_list.append(tagged_token)
    return tagged_token_list


def nltk_pos_tagger(token_list=None, include_math=False):
    """[NLTK built-in funcion]: Intepret a word for its part-of-speech (POS) in Penn Treebank (PTB) format"""
    """averaged_perceptron_tagger"""

    if type(token_list) is list:
        tagged_token_list = pos_correction(nltk.pos_tag(token_list))
    else:
        print "Unknown input type: ", type(token_list)
        return None

    #Assign SR ME-NP to all MATH part
    if not include_math:
        for i in range(len(tagged_token_list)):
            if "MATH" in tagged_token_list[i][0]:
                tagged_token_list[i] = (tagged_token_list[i][0], "NP-ME")

    return tagged_token_list


def tnt_pos_tagger(token_list=None):
    if type(token_list) is list:
        tagged_token_list = []
        me_sr_list = {}
        for i in range(len(token_list)):
            if "MATH_" in token_list[i]:
                me_sr_list[i] = ['S-ME', 'NP-ME', 'NML-ME']

        tag_list = tnt.predict(token_list, constrained_pos2tag_list=me_sr_list)
        for i in range(len(token_list)):
            tagged_token_list.append((token_list[i], tag_list[i]))
    else:
        print "Unknown input type: ", type(token_list)
        return None

    tagged_token_list = pos_correction(tagged_token_list)
    return tagged_token_list


if __name__ == "__main__":
    pass
