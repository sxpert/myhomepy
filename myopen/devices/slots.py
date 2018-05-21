# -*- coding: utf-8 -*-
from ..constants import *
from .baseslot import *


class Slots(object):
    def __init__(self, parent):
        self._parent = parent
        self._max_slots = MAX_SLOTS
        nb_slots = 0
        if parent is not None:
            ns = getattr(parent, VAR_NB_SLOTS, None)
            if ns is not None:
                self._max_slots = ns
            else:
                ns = 0
            nb_slots = ns
        self._slots = [None] * nb_slots

    def __str__(self):
        s = '<Slots (max=%d)' % (self._max_slots)
        for slot in self._slots:
            s += ' %s' % (str(slot))
        s += '>'
        return s

    # ========================================================================
    #
    # json loading and unloading
    #
    # ========================================================================

    def loads(self, data):
        if not isinstance(data, list):
            return False
        ok = True
        for sid in range(0, len(data)):
            slot = self._ensure_store_slot(sid + 1)
            ok &= slot.loads(data[sid])
        return ok

    def __to_json__(self):
        return self._slots

    # ========================================================================
    #
    # method to make sure the slots contain sensible objects
    #
    # ========================================================================

    def _ensure_slot(self, sid):
        if sid < MIN_SLOTS:
            return False
        if sid > self._max_slots:
            return False
        # only happens when parent is None
        if len(self._slots) < sid:
            # we don't have enough slots
            slots = self._slots
            slots += [None] * (sid - len(slots))
            self._slots = slots
        # everything is well, returns the slot
        return self._slots[sid - 1]

    def _ensure_store_slot(self, sid):
        slot = self._ensure_slot(sid)
        if slot is False:
            return None
        # we have something in the slot
        if slot is not None:
            return slot
        # create a new slot object
        slot_class = BaseSlot
        if self._parent is not None:
            slot_class = getattr(self._parent, VAR_SLOT_CLASS, BaseSlot)
        slot = slot_class()
        self._slots[sid - 1] = slot
        return slot

    # ========================================================================
    #
    # getters, setters and deleters
    #
    # ========================================================================

    def get_value(self, sid, key, default):
        slot = self._ensure_slot(sid)
        if slot is False:
            return None
        return slot.get_value(key, default)

    def set_value(self, sid, key, value):
        slot = self._ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.set_value(key, value)

    def del_value(self, sid, key):
        slot = self._ensure_slot(sid)
        if slot is False:
            return False
        # we got an empty slot, nothing to delete
        if slot is None:
            return True
        slot.del_value(key)

    def get_param(self, sid, key, default):
        slot = self._ensure_slot(sid)
        if slot is False:
            return None
        return slot.get_param(key, default)

    def set_param(self, sid, key, value):
        slot = self._ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.set_param(key, value)

    def del_param(self, sid, key):
        slot = self._ensure_slot(sid)
        if slot is False:
            return False
        # we got an empty slot, nothing to delete
        if slot is None:
            return True
        slot.del_param(key)

    # ========================================================================
    #
    # config-reactor functions
    #
    # ========================================================================

    def res_ko_value(self, sid, keyo, state):
        slot = self._ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.res_ko_value(keyo, state)

    def res_ko_sys(self, sid, sys, addr):
        slot = self._ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.res_ko_sys(sys, addr)

    def res_param_ko(self, sid, index, val_par):
        slot = self._ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.res_param_ko(index, val_par)
