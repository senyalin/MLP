# -*- coding: utf-8 -*-
from dec_util import tuple2list, get_me_idx_list
from nlp_util import parse_np_range_list, nltk_pos_tagger
from dec_ext_sample import DefExtSample
from feature_pattern import def_pattern_any
from bayesian_classifier import extract_dec_by_bayesian
from tokenization import tokenize_mwm_sent


def extract_def_by_pattern_from_token_list(token_list, enable_manual=True):
    """

    :param token_list:
    :return: list of dict {me_idx, me, def, np_range}
    """
    me_idx_list = get_me_idx_list(token_list)

    #print "TOKEN_LIST: ", token_list
    tagged_token_list = nltk_pos_tagger(token_list)
    #print tagged_token_list
    pos_tag_list = tuple2list(tagged_token_list, 1)
    np_range_list = parse_np_range_list(tagged_token_list)

    #print "NP: ", np_range_list

    # remove the NP of only one ME
    filter_np_range_list = []
    for np_range in np_range_list:
        if np_range is not None:
            contain_me = False
            for me_idx in me_idx_list:
                if np_range[0] <= me_idx <= np_range[1]:
                    contain_me = True
                    break
            if not contain_me:
                filter_np_range_list.append(np_range)
    np_range_list = filter_np_range_list

    ext_me_def_list = []
    for me_idx in me_idx_list:
        for np_range in np_range_list:
            des = DefExtSample()
            des.sent = {
                'token_list': token_list,
                'token_idx_list': range(len(token_list)),
                'pos_tag_list': pos_tag_list,
            }
            des.me_idx = me_idx
            des.def_ranges = [np_range]

            good_sample = False
            if enable_manual and def_pattern_any(des):
                good_sample = True

            if good_sample:
                ext_me_def_list.append({
                    'me_idx': me_idx,
                    'me': token_list[me_idx],
                    'def': ' '.join(token_list[np_range[0]: np_range[1] + 1]),
                    'np_range': np_range
                })

    # create combination of all the ME and all the NP for checking of the pattern
    return ext_me_def_list


def extract_dec_by_template(sent):
    """
    1. tokenize, and find ME locations
    2. PoS Tagging
    3. pass to the PoS tagger

    :param sent:
    :return:
    """
    token_list = tokenize_mwm_sent(sent)
    me_dec = {}
    me_dec_list = extract_def_by_pattern_from_token_list(token_list)
    #print "me_dec_list: ", me_dec_list
    for d in me_dec_list:
        if d['me'] not in me_dec:
            #print "{}: {}".format(d['me'], d['def'])
            me_dec[d['me']] = d['def']
    return me_dec


def extract_dec_by_pattern(sent):
    X = extract_dec_by_bayesian(sent)
    Y = extract_dec_by_template(sent)
    #print X
    #print Y
    for m_id in Y.keys():
        if m_id in X.keys():
            X[m_id] = [Y[m_id]]
    return X


# all in lower case
bad_def_list = [
    'it', 'which', 'the', 'this', 'they', 'there',
    'we', 'a', 'an', 'both', 'some', 'such that', 'he',
    'that', 'most', 'itself', 'one', 'two'
]


test_cases = [
    "Let MATH_1 be a point.",
    "Property MATH_1 MATH_2 MATH_3.",
    "Trees MATH_1 , MATH_2 , MATH_3 , MATH_4 , MATH_5 and MATH_6 are showed in Figure 2 .",
    "Let MATH_1, MATH_2, and MATH_3 be the longest path.",
    "MATH_1 stand for the graph.",
    "The final rotational kinetic energy is MATH_1.",
    "Substitute this value and the given value for MATH_1 into the above expression for MATH_2",
    "We now solve for MATH_1 and substitute known values into the resulting equation MATH_2",
    "The less energy goes into translation.",
    "Trees MATH_1222.2222_3-th, i.e., the ball's MATH_2 , MATH_3 , MATH_4 , MATH_5 and MATH_6 are showed in Figure 2 .",
    "Interestingly, the cylinder's radius MATH_1 and mass MATH_2 cancel, yielding MATH_3",
    "Suppose that the shared quantum state secret is MATH_1.",
    "Where MATH_1 is the product state of the first column of quantum bits held by Alice.",
    "Suppose MATH_1 is MATH_2.",
    "To achieved this constraint, a softmax transform maps latent vectors is MATH_1 onto defined by MATH_2.",
    "The distribution are drawn is MATH_1.",
    "Each weight MATH_1 is a fraction that denotes the membership of document MATH_2 in the topic MATH_3.",
    "MATH_14 is then called a ribbon disk."
]


if __name__ == "__main__":
    for sent in test_cases:
        print sent
        print extract_dec_by_pattern(sent)
        #print extract_dec_by_bayesian(sent)
