import numpy as np


class DefExtSample:
    """
    sample for definition extraction

    1. sentence
    2. ME index
    3. the noun phrase range
    """
    def __init__(self):
        # dict: token_list, token_id_list, pos_tag_list
        self.sent = None
        self.me_idx = None
        self.def_ranges = None  # inclusive ranges

    def get_me_token(self):
        for token, idx in zip(self.sent['token_list'], self.sent['token_idx_list']):
            if idx == self.me_idx:
                return token
        raise Exception("not exist")

    def get_def_token(self):
        def_str = ""
        for token, idx in zip(self.sent['token_list'], self.sent['token_idx_list']):
            for def_range in self.def_ranges:
                if def_range[0] <= idx <= def_range[1]:
                    def_str += token + ' '
        return def_str

    def __str__(self):
        return "{} => {}".format(self.get_me_token(), self.get_def_token())

    def get_left_token(self):
        for i, token_idx in enumerate(self.sent['token_idx_list']):
            if token_idx == self.me_idx-1:
                return self.sent['token_list'][i]
        return "<START>"

    def get_left_left_token(self):
        for i, token_idx in enumerate(self.sent['token_idx_list']):
            if token_idx == self.me_idx-2:
                return self.sent['token_list'][i]
        return "<START>"

    def get_me_idx(self):
        return self.me_idx

    def get_def_left_idx(self):
        # get the left bondary of the definition
        left_bounary_list = [r[0] for r in self.def_ranges]
        return np.min(left_bounary_list)

    def get_def_right_idx(self):
        # get the right bondary of the definition
        right_boundary_list = [r[1] for r in self.def_ranges]
        return np.max(right_boundary_list)

    def me_def_rel_pos(self):
        """
        relative position of the me to the definition
        :return:
            -1 means me on the left
            1 means me on the right
        """
        if self.get_me_idx() < self.get_def_left_idx():
            return -1
        elif self.get_me_idx() > self.get_def_right_idx():
            return 1
        else:
            return 0

    def get_tokens_between_me_def(self, filter_verb=False):
        """

        :return: list of tokens
        """
        rel_pos = self.me_def_rel_pos()
        if rel_pos == 0:
            #raise Exception("Should not call get tokens if the ME in the definition")
            # simply return empty for now
            return []

        start_idx = end_idx = -1  # inclusive boundary
        if rel_pos < 0:
            start_idx = self.get_me_idx()+1
            end_idx = self.get_def_left_idx()-1
        else:
            start_idx = self.get_def_right_idx()+1
            end_idx = self.get_me_idx()-1
        between_token_list = []
        for i, token_idx in enumerate(self.sent['token_idx_list']):
            if start_idx <= token_idx <= end_idx:
                if filter_verb and not self.sent['pos_tag_list'][i].startswith("VB"):
                    continue
                between_token_list.append(self.sent['token_list'][i])
        return between_token_list

    def _get_left(self, left_boundary, key, limit=None):
        left_token_list = []
        for i, token_idx in enumerate(self.sent['token_idx_list']):
            if token_idx < left_boundary:
                left_token_list.append(self.sent[key][i])
        if limit is None:
            return tuple(left_token_list)
        else:
            return tuple(left_token_list[-limit:])

    def _get_right(self, right_boundary, key, limit=None):
        right_token_list = []
        for i, token_idx in enumerate(self.sent['token_idx_list']):
            if token_idx > right_boundary:
                right_token_list.append(self.sent[key][i])
        if limit is None:
            return tuple(right_token_list)
        else:
            return tuple(right_token_list[:limit])

    def _get_tokens_left(self, boundary, limit=None):
        """
        :param boundary: not include the boundary
        :return:
        """
        left_token_list = self._get_left(
            boundary, "token_list", limit)
        return left_token_list

    def _get_tokens_right(self, right_boundary, limit=None):
        right_token_list = self._get_right(
            right_boundary, 'token_list', limit)
        return right_token_list

    def get_tokens_left_me_def(self):
        """
        get the tokens on the left of the ME-Def pair
        :return:
        """
        left_boundary = self.get_me_idx()
        left_boundary = min(left_boundary, self.get_def_left_idx())
        return self._get_tokens_left(left_boundary)

    def get_token_left_def(self, limit=None):
        """
        get tokens on the left of def

        :return:
        """
        left_boundary = self.get_def_left_idx()
        return self._get_tokens_left(left_boundary, limit)

    def get_token_right_def(self, limit=None):
        right_boundary = self.get_def_right_idx()
        return self._get_tokens_right(right_boundary, limit)

    def get_tokens_right_me_def(self):
        """

        :return:
        """
        right_boundary = self.get_me_idx()
        right_boundary = max(right_boundary, self.get_def_right_idx())
        return self._get_tokens_right(right_boundary)


