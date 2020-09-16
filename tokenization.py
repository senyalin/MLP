import re
import string


def split_by_me(sent):
    if sent.count("$") % 2 != 0:
        if isinstance(sent, unicode):
            msg = "Sent chunking error {}".format(sent.encode('utf-8', 'ignore'))
        else:
            msg = "Sent chunking error {}".format(sent)
        #me_analysis_error_logger.error(msg)
        return []
    interval_list = []
    for m in re.finditer("(\$(\s|\S)*?\$)", sent):
        interval_list.append((m.start(), m.end()))
    if len(interval_list) == 0:
        return [sent]
    chunks = []
    if interval_list[0][0] > 0:
        chunks.append(sent[:interval_list[0][0]])
    for i in range(len(interval_list)-1):
        chunks.append(sent[interval_list[i][0]:interval_list[i][1]])
        chunks.append(sent[interval_list[i][1]: interval_list[i+1][0]])
    chunks.append(sent[interval_list[-1][0]:interval_list[-1][1]])
    if interval_list[-1][1] < len(sent)-1:
        chunks.append(sent[interval_list[-1][1]:])
    #print chunks
    return chunks


def split_by_delimeter(chunk):
    if chunk.startswith("$") and chunk.endswith('$'):
        return [chunk]
    #words = re.split(",|;|\.| ", chunk)
    words = chunk.split(" ")
    res_word_list = []
    for w in words:
        if w == "":
            continue
        if len(w) > 1:
            while len(w) > 1:
                if w[0] in string.punctuation:
                    res_word_list.append(w[0])
                    w = w[1:]
                else:
                    break
            rev_punct_list = []
            while len(w) > 1:
                if w[-1] in string.punctuation:
                    rev_punct_list.append(w[-1])
                    w = w[:-1]
                else:
                    break
            #print rev_punct_list
            res_word_list.append(w)
            res_word_list.extend(reversed(rev_punct_list))
        else:
            res_word_list.append(w)
    res_word_list = [w for w in res_word_list if w != ""]
    return res_word_list


def tokenize_mwm_sent(sent):
    """
    tokenization of MEP sentence

    :param sent:
    :return:
    """
    chunk_list = split_by_me(sent)
    word_list = []
    for chunk in chunk_list:
        words = split_by_delimeter(chunk)
        word_list.extend(words)
    return word_list


if __name__ == "__main__":
    pass
