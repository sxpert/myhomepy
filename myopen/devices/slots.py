# -*- coding: utf-8 -*-
from ..constants import (
    MAX_SLOTS, MIN_SLOTS,
    VAR_NB_SLOTS, VAR_SLOT_CLASS,
)
from core.logger import LOG_ERROR
from .baseslot import BaseSlot


class Slots(object):
    def __init__(self, parent):
        self.parent = parent
        self.log = parent.log
        self.max_slots = MAX_SLOTS
        nb_slots = 0
        if parent is not None:
            ns = getattr(parent, VAR_NB_SLOTS, None)
            if ns is not None:
                self.max_slots = ns
            else:
                ns = 0
            nb_slots = ns
        self.slots = [None] * nb_slots

    def __str__(self):
        s = '<Slots (max=%d)' % (self.max_slots)
        for slot in self.slots:
            s += ' %s' % (str(slot))
        s += '>'
        return s

    def __len__(self):
        return len(self.slots)

    # ========================================================================
    #
    # front-end related 
    #
    # ========================================================================

    @property
    def slot_class(self):
        if self.parent is not None:
            return getattr(self.parent, VAR_SLOT_CLASS, BaseSlot)
        return BaseSlot

    @property
    def web_data(self):
        slots = []
        for slot in self.slots:
            slots.append(slot.web_data)
        return slots

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
            slot = self.ensure_store_slot(sid + 1)
            slot_ok = slot.loads(data[sid])
            # default loader ?
            if not slot_ok:
                self.log('Loading slot %d => %s appears to have failed, launching default loader ?' % (sid, str(data[sid])), LOG_ERROR)
            ok &= slot_ok
        return ok

    def __to_json__(self):
        return self.slots

    # ========================================================================
    #
    # method to make sure the slots contain sensible objects
    #
    # ========================================================================

    def ensure_slot(self, sid):
        if sid < MIN_SLOTS:
            return False
        if sid > self.max_slots:
            return False
        # only happens when parent is None
        if len(self.slots) < sid:
            # we don't have enough slots
            slots = self.slots
            slots += [None] * (sid - len(slots))
            self.slots = slots
        # everything is well, returns the slot
        return self.slots[sid - 1]

    def ensure_store_slot(self, sid):
        slot = self.ensure_slot(sid)
        if slot is False:
            return None
        # we have something in the slot
        if slot is not None:
            return slot
        # create a new slot object
        sc = self.slot_class
        slot = sc(self)
        self.slots[sid - 1] = slot
        return slot

    # ========================================================================
    #
    # getters, setters and deleters
    #
    # ========================================================================

    def get_value(self, sid, key, default):
        slot = self.ensure_slot(sid)
        if slot is False:
            return None
        return slot.get_value(key, default)

    def set_value(self, sid, key, value):
        slot = self.ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.set_value(key, value)

    def del_value(self, sid, key):
        slot = self.ensure_slot(sid)
        if slot is False:
            return False
        # we got an empty slot, nothing to delete
        if slot is None:
            return True
        slot.del_value(key)

    def get_param(self, sid, key, default):
        slot = self.ensure_slot(sid)
        if slot is False:
            return None
        return slot.get_param(key, default)

    def set_param(self, sid, key, value):
        slot = self.ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.set_param(key, value)

    def del_param(self, sid, key):
        slot = self.ensure_slot(sid)
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
        slot = self.ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.res_ko_value(keyo, state)

    def res_ko_sys(self, sid, sys, addr):
        slot = self.ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.res_ko_sys(sys, addr)

    def res_param_ko(self, sid, index, val_par):
        slot = self.ensure_store_slot(sid)
        if slot is False:
            return False
        return slot.res_param_ko(index, val_par)
