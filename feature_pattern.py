# -*- coding: utf-8 -*-
"""
pattern based features
TODO, test each function
"""
import re


def def_pattern_common(dec_ext_sample, between_tokens_pattern_list):
    """

    :param dec_ext_sample:
    :param between_tokens_pattern_list:
    :return:
    """
    existing_token_list = dec_ext_sample.get_tokens_between_me_def()
    for between_tokens_pattern in between_tokens_pattern_list:
        if existing_token_list == between_tokens_pattern:
            return True
    return False


def def_pattern_1(dec_ext_sample):
    """
    ME denote(s?)|mean(s?) [the] DEC
    ME stand(s?) for [the] DEC
    :param dec_ext_sample:
    :return:
    """
    if def_pattern_common(dec_ext_sample, [
        ["denote"],
        ["denote", "the"],
        ["mean"],
        ["mean", "the"],
        ["denotes"],
        ["denotes", "the"],
        ["means"],
        ["means", "the"],
        ["stand", "for"],
        ["stand", "for", "the"],
        ["stands", "for"],
        ["stands", "for", "the"],
        ['represents'],
        ['represents', 'the'],
        ['represent'],
        ['represent', 'the']
    ]):
        return 1
    return 0


def def_pattern_2(dec_ext_sample):
    """
    ME is|are [the] DEC
    :param dec_ext_sample:
    :return:
    """
    if def_pattern_common(dec_ext_sample, [
        ["is"],
        ["is", "the"],
        ["are"],
        ["are", "the"],
    ]):
        return 1
    return 0


def def_pattern_3(dec_ext_sample):
    """
    ME is|are denoted by [the] DEC
    ME [is|are] denoted|defined|given as|by [the] DEC
    is|are : optional
    :param dec_ext_sample:
    :return:
    """
    if def_pattern_common(dec_ext_sample, [
        ["is", "denoted", "by"],
        ["are", "denoted", "by"],
        ["is", "denoted", "as"],
        ["are", "denoted", "as"],

        ["is", "defined", "by"],
        ["are", "defined", "by"],
        ["is", "defined", "as"],
        ["are", "defined", "as"],

        ["is", "given", "by"],
        ["are", "given", "by"],
        ["is", "given", "as"],
        ["are", "given", "as"],

        ["is", "denoted", "by", "the"],
        ["are", "denoted", "by", "the"],
        ["is", "denoted", "as", "the"],
        ["are", "denoted", "as", "the"],

        ["is", "defined", "by", "the"],
        ["are", "defined", "by", "the"],
        ["is", "defined", "as", "the"],
        ["are", "defined", "as", "the"],

        ["is", "given", "by", "the"],
        ["are", "given", "by", "the"],
        ["is", "given", "as", "the"],
        ["are", "given", "as", "the"],
    ]):
        return 1
    return 0


def def_pattern_4(dec_ext_sample):
    """
    let ME be denoted by [the] DEC
    :param dec_ext_sample:
    :return:
    """
    left_token = dec_ext_sample.get_left_token()
    if left_token not in ['let', "Let"]:
        return 0
    if def_pattern_common(dec_ext_sample, [
        ["be", "denoted", "by"],
        ["be", "denoted", "by", "the"],
    ]):
        return 1
    return 0


def def_pattern_5(dec_ext_sample):
    """
    denote (as|by) ME DEC
    :param dec_ext_sample:
    :return:
    """
    left_token = dec_ext_sample.get_left_token()
    left_left_token = dec_ext_sample.get_left_left_token()
    good_prefix = False
    if re.match("denote", left_token, re.I):
        good_prefix = True
    if re.match("denote", left_left_token, re.I) and re.match("(as|by)", left_token, re.I):
        good_prefix = True
    if not good_prefix:
        return 0
    if dec_ext_sample.get_me_idx() +1 == dec_ext_sample.get_def_left_idx():
        return 1
    return 0


def def_pattern_6(dec_ext_sample):
    """
    let|set ME denote|denotes|be DEC
    :param dec_ext_sample:
    :return:
    """
    left_token = dec_ext_sample.get_left_token()
    if not re.match("(let|set)", left_token, re.I):
        return 0
    if def_pattern_common(dec_ext_sample, [
        ['denote'],
        ['be'],
    ]):
        return 1
    return 0


def def_pattern_7(dec_ext_sample):
    """
    extension of pattern def_pattern_1
    DEC (OTHER_ME)* , and|or ME
    (OTHER_ME)*, and ME ... are|be DEC
    :param dec_ext_sample:
    :return:
    """
    cc_words = ['and', 'or']
    vb_words = ['are', 'be']
    between_tokens = dec_ext_sample.get_tokens_between_me_def()
    for token in between_tokens:
        if not token.startswith("MATH_") and ',' not in token and token not in cc_words and token not in vb_words:
            return 0
    return 1


def def_pattern_8(dec_ext_sample):
    """
    extension of pattern def_pattern_1
    DEC (OTHER_ME)* ME
    :param dec_ext_sample:
    :return:
    """
    between_tokens = dec_ext_sample.get_tokens_between_me_def()
    for token in between_tokens:
        if not token.startswith("MATH_"):
            return 0
    return 1


def def_pattern_9(dec_ext_sample):
    """
    DEC ME
    :param dec_ext_sample:
    :return:
    """
    r = 1 if dec_ext_sample.get_def_right_idx()+1 == dec_ext_sample.get_me_idx() else 0
    return r


def def_pattern_0(dec_ext_sample):
    """
    ME DEC
    :param dec_ext_sample:
    :return:
    """
    r = 1 if dec_ext_sample.get_def_left_idx()-1 == dec_ext_sample.get_me_idx() else 0
    return r


confirmed_pattern_list = [
    "...Let... ME ...be... DEC ...",
    "...Let... ME ...denote... DEC ...",
    "...let... ME ...be... DEC ...",
    "...use... ME ...denote... DEC ...",
    "... ME ...to...denote... DEC ...",
    "...Let... ME ...represent... DEC ...",
    "... ME ...refers...to... DEC ...",
    "... ME ...stands...for... DEC ...",
    "...with... ME ...being... DEC ...",
    "...represented...by... DEC ... ME ...",
    "...takes...as... DEC ... ME ...",
    "...Let...denote... DEC ... ME ...",
    "...let... ME ...denote... DEC ...",
    "...denoted...by... ME ... DEC ...",
    "...denoted...by... DEC ... ME ...",
    "... ME ...is...called... DEC ...",
    "...denote...by... ME ... DEC ...",
    "...define... DEC ... ME ...as...",
    "... DEC ...denote...by... ME ...",
    "... DEC ...denoted...by... ME ...",
    "...denote... DEC ...by... ME ...",
    "...defined...as... DEC ... ME ...",

    # new patterns after more sample are introduced.
    "...denote... DEC ...as... ME ...",
    "...Denote... ME ...as... DEC ...",
    "...define... ME ...as... DEC ...",
    "...denote... ME ...as... DEC ...",
    "...with... ME ...denoting... DEC ...",
    "...Denote...by... ME ... DEC ...",
    "...use... ME ...represent... DEC ...",

    # 6/7
    "...(... ME ...)... DEC ...",
]


existing_feature_list = [
    def_pattern_1,
    def_pattern_2,
    def_pattern_3,
    def_pattern_4,
    def_pattern_5,
    def_pattern_6,
    def_pattern_7,
    def_pattern_8,
]


def def_pattern_any(dec_ext_sample):
    """

    :param dec_ext_sample:
    :return: return True if any of them is satisfied
    """
    for def_pattern_feature in existing_feature_list:
        if def_pattern_feature(dec_ext_sample):
            return 1
    return 0


def dump_latex_table():
    existing_pattern_str_list = [
        "DEC ME",
        "ME denote / mean / stand for DEC",
        "ME DEC",
        "ME is denoted / defined / given by DEC",
        "ME is / are DEC" ,
        "Let ME be denoted by DEC",
        "DEC (ME) * ME" ,
        "Let / Set ME denote / be DEC",
        "denote (as / by) ME DEC"
    ]

    col_width = 3
    for i, pattern_str in enumerate(existing_pattern_str_list):
        if (i+1) % col_width == 0:
            print pattern_str + "\\\\ "
        else:
            print pattern_str + "& ",

    mined_pattern_list = [
        'let ME be/define DEC',
        'use ME as DEC',
        'use ME [to]* denote/represent DEC',
        'with ME being/denoting DEC',
        'ME refer[s]* to DEC',
        'refer ME as DEC',
        'refer DEC as ME',
        'write ME for DEC',
        'ME is called DEC',
        "DEC represented by ME",
        "ME corresponding to DEC",
        "ME (DEC)",
        'DEC denote[d]* by/as ME',
        'define/denote ME as DEC',
        'define/denote DEC as ME',
    ]

    col_width = 3
    for i, pattern_str in enumerate(mined_pattern_list):
        if (i + 1) % col_width == 0:
            print pattern_str + "\\\\ "
        else:
            print pattern_str + "& ",


if __name__ == "__main__":
    #dump_latex_table()
    print existing_feature_list
    def_pattern_7([('MATH_1', 'NP-ME'), ('and', 'CC'), ('MATH_2', 'NP-ME'), ('are', 'VBP'), ('numbers', 'NNS'), ('.', '.')])
