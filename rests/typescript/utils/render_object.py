import json

from rests.typescript.utils.literal import Literal


def _render_value(val):
    if isinstance(val, Literal):
        return str(val)
    if val == 'undefined':
        return val
    if val is None:
        return 'null'
    if val == False:
        return 'false'
    if val == True:
        return 'true'
    if isinstance(val, (dict, list)):
        return json.dumps(val)
    if isinstance(val, str):
        return "\'" + val + "\'"

    return val


def render_object(object_: dict):
    return "{" + ", ".join([f"{k}: {_render_value(v)}" for k, v in object_.items()]) + "}"