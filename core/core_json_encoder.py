import json as system_json


class CoreJsonEncoder(system_json.JSONEncoder):
    def default(self, obj):     # pylint: disable=E0202
        if '__to_json__' in dir(obj):
            return obj.__to_json__()
        else:
            return system_json.JSONEncoder.default(self, obj)


def dumps(obj, indent=None):
    return system_json.dumps(obj,
                             cls=CoreJsonEncoder,
                             indent=indent)
