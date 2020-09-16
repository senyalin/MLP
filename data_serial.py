# -*- coding: utf-8 -*-
import codecs
import os
import pickle
import json


def load_general(file_path):
    if file_path.endswith("json"):
        return load_json(file_path)
    elif file_path.endswith("pkl"):
        return load_serialization(file_path)
    elif file_path.endswith("txt"):
        return load_txt(file_path)
    else:
        raise Exception("unknown file extension")


def load_serialization(file_path):
    if not os.path.isfile(file_path):
        raise Exception("{} file not exist".format(file_path))
    return pickle.load(open(file_path, "rb"))


def load_json(file_path):
    return json.load(open(file_path))


def load_txt(file_path):
    with open(file_path) as f:
        return f.readlines()


def encode2base64(data):
    return codecs.encode(pickle.dumps(data), "base64").decode()


def decode_from_base64(data):
    return pickle.loads(codecs.decode(data.encode(), "base64"))
