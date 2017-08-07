import logging
import string
from datetime import datetime

log = logging.getLogger(__name__)


def serialize(value):
    """Very simple helper function which returns a stringified version
    of the given python value."""
    if value is None:
        return ""
    if isinstance(value, unicode):
        return value
    if isinstance(value, int):
        return unicode(value)
    if isinstance(value, float):
        return unicode(value)
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, bool):
        # use 1 and 0 here to be able to set this values on import,
        # "True" and "False" will fail.
        return value and "1" or "0"
    # Now handle relations, 3 cases: empty, 1 item and 2+ items.
    if isinstance(value, list) and not value:
        return []
    # cannot import BaseItem here, so check for BaseItem with hasattr.
    if isinstance(value, list) and hasattr(value[0], 'id'):
        return sorted([v.id for v in value])
    if hasattr(value, 'id'):
        return [value.id]
    # Even if Ringo does not have a bytearray type yet the serialize
    # method supports it to convert the given value into unicode
    if isinstance(value, bytearray):
        return value.decode("utf-8")
    log.warning("Unhandled type '%s'. "
                "Using default and converting to unicode" % type(value))
    return unicode(value)

def safestring(unsafe):
    """Returns a 'safe' version of the given string. All non ascii chars
    and other chars are removed """
    valid_chars = "_%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in unsafe if c in valid_chars)


def dynamic_import(cl):
    d = cl.rfind(".")
    classname = cl[d + 1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)
