# -*- coding: utf-8 -*-

from ..constants import *

# ========================================================================
#
# parameters loading and checking
#
# ========================================================================


def split_byte_addr(addr):
    a = addr // 16
    pl = addr % 16
    return (a, pl)


def check_byte_addr(addr):
    # NOTE: MyHome_Suite authorizes :
    # A 0-10
    # PL 0-15
    # this violates the official docs

    # if addr == 0:
    #     return False
    split = split_byte_addr(addr)
    a, pl = split
    if a not in range(0, 11):
        return False
    if pl not in range(0, 16):
        return False
    return True


def check_value(value, tests):
    valid = False

    for t in tests:
        if callable(t):
            v = t(value)
        else:
            v = value in t
        valid |= v
    if valid:
        return value
    return None


def get_param(data, index):
    if not isinstance(data, dict):
        return False
    params = data.get(VAR_PARAMS_KEY, None)
    if params is None:
        return None
    # params must be a dict
    if not isinstance(params, dict):
        return None
    # data is normally loaded from json, where keys are
    # only able to be strings
    if isinstance(index, int):
        index = str(index)
    # index must be a string by then
    if not isinstance(index, str):
        return None
    # index must be a string representing an integer
    if not index.isdecimal():
        return None
    # get parameter
    value = params.get(index, None)
    return value


def get_value(data, name):
    if not isinstance(data, dict):
        return None
    if not isinstance(name, str):
        return None
    value = data.get(name, None)
    return value


def get_check_value(data, name, values, warn=True):
    value = get_value(data, name)
    if value is None:
        return None
    v = check_value(value, values)
    if v is None and warn:
        print(
            'get_check_value : invalid value %s for var %s '
            'expected %s' % (value, name, str(values)))
    return v


def get_check(data, index, ivalues, name, nvalues, warn=True):
    value = get_param(data, index)
    if value is not None:
        v = check_value(value, ivalues)
        if v is None and warn:
            print(
                'get_check : invalid param %s %s'
                % (str(index), str(value)))
        value = v
    if value is None:
        value = get_value(data, name)
    if value is None:
        if warn:
            print('get_check : '
                  'unable to find valid param(%s) or %s in %s'
                  % (str(index), str(name), str(data)))
        return None
    v = check_value(value, nvalues)
    if v is None and warn:
        print('get_check : Found invalid value %s for %s'
              % (str(value), str(name)))
    return value
