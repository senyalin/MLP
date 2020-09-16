# -*- coding: utf-8 -*-
"""
This is the code for Constraint Labeling Models (CLM)
"""
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from data_serial import load_general
from dec_util import between_me_and_np, get_me_list, get_np
from nlp_util import nltk_pos_tagger, parse_np_range_list
from tokenization import tokenize_mwm_sent


def extract_dec_by_bayesian(sent=None):
    """
    Process dec extraction by tagged sentence
    :return:
    """
    token_list = tokenize_mwm_sent(sent)
    #print "token_list: ", token_list
    me_dec = {}
    tagged_token_list = nltk_pos_tagger(token_list)
    #print "tagged_token_list: ", tagged_token_list

    if tagged_token_list is not None:
        me_list = get_me_list(token_list)
        #print "me_list: ", me_list
        np_range_list = parse_np_range_list(tagged_token_list)
        #print "np_range_list: ", np_range_list
        #dec_list = get_np(tagged_token_list)
    else:
        me_list = []
        np_range_list = []

    for me in me_list:
        np_list = dec_prediction(tagged_token_list, me, np_range_list)
        if me not in me_dec:
            me_dec[me] = {}
        me_dec[me] = np_list

    return me_dec


def get_prior(feature_type=None):
    PROJECT_FOLDER = os.path.dirname(os.path.realpath(__file__))
    if feature_type is None:
        return {"RHS": {"Y": 0.5, "N": 0.5}, "LHS": {"Y": 0.5, "N": 0.5}}
    elif feature_type == "dist":
        fpath = "{}/model/{}_prior.json".format(PROJECT_FOLDER, feature_type)
        return load_general(fpath)
    elif feature_type == "word":
        fpath = "{}/model/{}_prior.json".format(PROJECT_FOLDER, feature_type)
        return load_general(fpath)
    elif feature_type == "post":
        fpath = "{}/model/{}_prior.json".format(PROJECT_FOLDER, feature_type)
        return load_general(fpath)
    else:
        print "Unknown feature type: ", feature_type
        return {"RHS": {"Y": 0.5, "N": 0.5}, "LHS": {"Y": 0.5, "N": 0.5}}


def get_likelihood(feature_type=None):
    PROJECT_FOLDER = os.path.dirname(os.path.realpath(__file__))
    if feature_type is None:
        return {"RHS": {}, "LHS": {}}
    elif feature_type == "dist":
        fpath = "{}/model/{}_feature.json".format(PROJECT_FOLDER, feature_type)
        return load_general(fpath)
    elif feature_type == "word":
        fpath = "{}/model/{}_feature.json".format(PROJECT_FOLDER, feature_type)
        return load_general(fpath)
    elif feature_type == "post":
        fpath = "{}/model/{}_feature.json".format(PROJECT_FOLDER, feature_type)
        return load_general(fpath)
    else:
        print "Unknown feature type: ", feature_type
        return {"RHS": {}, "LHS": {}}


def feature_extraction(tkn_list=[], f_type=None):
    """
    Extract feature based
    :return: LHS/RHS, evident_list
    """
    if not tkn_list:
        print "Please input a list of tokens between ME and DEC"
        return None, None
    else:
        evid_list = []
        if tkn_list[0] == "ME" and tkn_list[-1] == "NP":
            dec_type = "RHS"
        elif tkn_list[0] == "NP" and tkn_list[-1] == "ME":
            dec_type = "LHS"

        if f_type == "word" or f_type == "post":
            for tkn in tkn_list:
                if "ME" in tkn or "NP" in tkn:
                    pass
                elif "MATH_" in tkn or "-ME" in tkn:
                    pass
                else:
                    evid_list.append(tkn)

            if not evid_list:
                evid_list.append("-NONE-")
        elif f_type == "dist":
            for tkn in tkn_list:
                if "ME" in tkn or "NP" in tkn:
                    pass
                else:
                    evid_list.append(tkn)
            if not tkn_list or tkn_list[0] == "-NONE-":
                evid_list = [1]
            else:
                evid_list = [len(evid_list)+1]
        else:
            print "Unknown feature type: ", f_type
            return None, None
        return dec_type, evid_list


def dec_prediction(tagged_token_list, me, np_range_list):
    """

    :return:
    """
    dec_list = []

    for np_range in np_range_list:
        np = get_np(tagged_token_list, np_range)

        vote = 0
        ##print "{}: {}".format(me, dec)
        dist_pattern = between_me_and_np(tagged_token_list, me, np_range, "dist")
        #print "dist_pattern: ", dist_pattern
        d_type, e_list = feature_extraction(dist_pattern, "dist")
        ##print d_type, e_list
        dist_posterior = bayes_inference(d_type, e_list, "dist")
        ##print dist_posterior
        if dist_posterior > 0:
            vote += 1

        word_pattern = between_me_and_np(tagged_token_list, me, np_range, "word")
        d_type, e_list = feature_extraction(word_pattern, "word")
        ##print d_type, e_list
        word_posterior = bayes_inference(d_type, e_list, "word")
        ##print word_posterior
        if word_posterior > 0:
            vote += 1

        post_pattern = between_me_and_np(tagged_token_list, me, np_range, "post")
        d_type, e_list = feature_extraction(post_pattern, "post")
        ##print d_type, e_list
        post_posterior = bayes_inference(d_type, e_list, "post")
        ##print post_posterior
        if post_posterior > 0:
            vote += 1

        if vote >= 2 and np not in dec_list:
            dec_list.append(np)

    #print "FINALE {}: {}".format(me, dec_cand)
    return dec_list


def bayes_inference(d_type=None, e_list=None, f_type=None):
    if d_type is None or e_list is None or f_type is None:
        #print "Missing Parameters!!!"
        #print d_type, e_list, f_type
        return
    else:
        model = get_likelihood(f_type)
        prior = get_prior(f_type)

    # Inference Phase
    E = e_list              # Evidence List
    alpha = 0.001           # Smoothing Parameter
    total_E = len(model[d_type].keys())

    # print test_data['data'][i], latex_symbol_extraction(test_data['data'][i])
    E_H = {'Y': 1.0, 'N': 1.0}
    for elem in E:
        if elem in model[d_type].keys():
            E_Y = model[d_type][elem]['Y']
            E_N = model[d_type][elem]['N']
            E_H['Y'] *= (float(E_Y)+alpha) / (float(E_Y)+float(E_N)+alpha*(total_E+1.0))
            E_H['N'] *= (float(E_N)+alpha) / (float(E_Y)+float(E_N)+alpha*(total_E+1.0))
        else:
            E_H['Y'] *= alpha / (alpha*(total_E+1.0))
            E_H['N'] *= alpha / (alpha*(total_E+1.0))

    # Posterior
    if not E:
        likelihood_ratio = 0.0
    elif E_H['N']*prior[d_type]['N'] == 0:
        likelihood_ratio = (E_H['Y'] * prior[d_type]['Y']) / alpha
    else:
        likelihood_ratio = (E_H['Y']*prior[d_type]['Y']) / (E_H['N']*prior[d_type]['N'])

    if likelihood_ratio >= 1:
        return round(likelihood_ratio, 2)
    else:
        return 0.0


if __name__ == "__main__":
    print get_prior("dist")
    print get_likelihood("dist")
    print get_likelihood("word")
    print get_likelihood("post")
