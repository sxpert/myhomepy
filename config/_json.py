# -*- coding: utf-8 -*-

import json


class Json(object):
    def load(self, data):
        # do nothing
        pass

    def serialize(self):
        return None

    def json(self):
        return json.dumps(self.serialize(), indent=4)


