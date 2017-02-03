# -*- coding: utf-8 -*-
""" Valitation utilities

This module implements a set of helpers function to facilitate
repetitive validation task with marshmallow library. 

"""
import ipaddress
from marshmallow import ValidationError


def _count(db, model, field, value):
    kwargs = {field: value}
    count = db.session.query(model). \
        filter_by(**kwargs).count()
    return count


def validate_unique(db, model, field, value):
    """
    check for duplicate fields values

    Keyword arguments:
    db    -- the sqlalchemy database
    model -- the sqlalchemy model
    field -- the attribute of model to be checked
    value -- the value to be checked
    """
    count = _count(db, model, field, value)
    if(count > 0):
        raise ValidationError(
            'El "{}" {} ya existe'.format(field, value))


def validate_unique_update(db, model, field, value, object):
    """
    check for duplicate fields values only if object.field != value
    that is: if object.field == value means that we want to keep the
    field the same, so we don't check any thing

    Keyword arguments:
    db     -- the sqlalchemy database
    model  -- the sqlalchemy model
    field  -- the attribute of model to be checked
    value  -- the value to be checked
    object -- the object to be updated
    """
    if getattr(object, field) != value:
        validate_unique(db, model, field, value)


def validate_exists(db, model, field, value):
    count = _count(db, model, field, value)
    if(count == 0):
        raise ValidationError(
            'El "{}" {} no existe'.format(field, value))


def validate_ip(value):
    try:
        ipaddress.ip_address(value)
    except ValueError:
        raise ValidationError(
            '"{}" no es una IP válida '.format(value))
