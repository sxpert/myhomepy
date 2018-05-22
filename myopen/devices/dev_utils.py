# -*- coding: utf-8 -*-

from ..constants import VAR_PARAMS_KEY

# ========================================================================
#
# parameters loading and checking
#
# ========================================================================


def split_byte_addr(addr):
    a = addr // 16
    pl = addr % 16
    return (a, pl)


def split_long_addr(addr):
    l = len(addr)
    if l == 2:
        s_a = addr[0]
        s_pl = addr[1]
    elif l == 4:
        s_a = addr[0:2]
        s_pl = addr[2:4]
    else:
        print('split_long_addr ERROR: unknown format length %d \'%s\''
              % (l, addr))
        return (None, None,)
    return (int(s_a), int(s_pl))


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


def check_value(value, values):
    if value in values:
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


def get_check_value(data, name, ivalues, nvalues, warn=True):
    value = get_value(data, name)
    if value is None:
        return None
    v = check_value(value, ivalues)
    if v is not None:
        return v
    v = check_value(value, nvalues)
    if v is not None:
        i = nvalues.index(v)
        value = ivalues[i]
        print('found value %s as index %d -> returning %d' % (v, i, value))
        return value
    return v


def get_check(data, index, name, ivalues, nvalues, warn=True):
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
    if isinstance(value, str):
        if value.isdecimal():
            value = int(value)
            v = check_value(value, ivalues)
            if v is not None:
                return ivalues.index(v)
        if nvalues is not None:
            v = check_value(value, nvalues)
            if v is None:
                if warn:
                    print('get_check : Found invalid value %s for %s'
                          % (str(value), str(name)))
            else:
                # we return the index in the array of strings
                return nvalues.index(v)
    return value


def map_value(value, values):
    if value in values:
        return values.index(value)
    print('map_value ERROR => value %s not in %s' % (value, str(values)))
    return None


def json_find_value(value, values):
    try:
        if value >= 0 and value < len(values):
            return values[value]
    except TypeError:
        pass
    print('invalid index %s %s' % (value, str(values)))
    raise IndexError
