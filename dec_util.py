# -*- coding: utf-8 -*-
from nlp_util import stemmer


def get_np(tagged_token_list=None, np_range=None):
    word_list = []
    if tagged_token_list is not None and np_range is not None:
        for i in range(np_range[0], np_range[1]+1):
            word_list.append(tagged_token_list[i][0])
    return " ".join(word_list)


def get_me_idx(token_list, me):
    for i in range(len(token_list)):
        if me in token_list[i]:
            return i
    return None


def get_me_list(token_list=None):
    me_list = []
    if token_list is not None:
        for i, token in enumerate(token_list):
            if token.startswith("MATH_") or token.startswith("ME_"):
                if token not in me_list:
                    me_list.append(token)
    return me_list


def get_me_idx_list(token_list=None):
    me_idx_list = []
    if token_list is not None:
        for i, token in enumerate(token_list):
            if token.startswith("MATH_") or token.startswith("ME_"):
                me_idx_list.append(i)
    return me_idx_list


def between_me_and_np(tagged_token_list=None, me=None, np_range=None, f_type=None):
    """
    Retrieve all tokens between ME and DEC
    :param seq:
    :return:
    """
    sub_token = []
    if tagged_token_list is None or me is None or np_range is None or f_type is None:
        print "[ERROR] Missing parameters~"
        print "tagged_token_list: {}".format(tagged_token_list)
        print "me: {}".format(me)
        print "np_range: {}".format(np_range)
        print "f_type: {}".format(f_type)
    else:
        tkn_list = []
        word_list = tuple2list(tagged_token_list, 0)
        me_idx = get_me_idx(word_list, me)
        np = get_np(tagged_token_list, np_range)

        if f_type == "word":
            # Take Word feature
            for wrd in word_list:
                if "MATH_" not in wrd:
                    tkn_list.append(stemmer(wrd))
                else:
                    tkn_list.append(wrd)
        elif f_type == "post":
            # Take POS tag feature
            tkn_list = tuple2list(tagged_token_list, 1)
        else:
            tkn_list = word_list
        if np_range:
            if min(np_range) > me_idx:
                sub_token.append("ME")
                sub_token.extend(tkn_list[me_idx+1:np_range[0]])
                sub_token.append("NP")
            elif max(np_range) < me_idx:
                sub_token.append("NP")
                sub_token.extend(tkn_list[np_range[1]+1:me_idx])
                sub_token.append("ME")
            else:
                print "Special cases where ME is at ", me_idx, " and NP is at ", np_range
        else:
            print "Unable to locate [{}] in the sentence".format(np)
    return sub_token


def tuple2list(tup_list=[], i=0):
    """
    Convert all i-th elements in tuple to a list
    :param tup_list: list of tuples
    :param i: index
    :return:  list of tokens
    """
    try:
        return [tup[i] for tup in tup_list]
    except Exception as e:
        print(e)
        return []


def list2string(tkn_list=[]):
    '''Convert a list of tokens to string'''
    """
    :param tkn_list: list of tokens
    :return:  string
    """
    return " ".join(tkn_list)


def tuple2string(tup_list=[], i=0):
    '''Convert a list of tuples to string'''
    """
    :param tup_list: list of tuples
    :param i: index
    :return:  string
    """
    return list2string(tuple2list(tup_list, i))


if __name__ == "__main__":
    tkn = [('Interestingly', 'RB'), (',', ','), ('the', 'DT'), ("cylinder's", 'NN'), ('radius', 'NN'),
           ('MATH_1', 'NP-ME'), ('and', 'CC'), ('mass', 'NN'), ('MATH_2', 'NP-ME'), ('cancel', 'NN'),
           (',', ','), ('yielding', 'VBG'), ('MATH_3', 'NP-ME')]
    print tuple2string(tkn)
    print tuple2list(tkn)
