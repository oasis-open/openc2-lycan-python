import json
import copy
from . import exceptions
from .core import OPENC2_OBJ_MAPS


def _get_data_info(data, component_type, allow_custom=False):
    obj = _get_dict(data)
    obj = copy.deepcopy(obj)
    try:
        _type = list(obj.keys())[0]
        nsid = _type
        _specifiers = list(obj.values())[0]
    except IndexError:
        raise exceptions.ParseError(
            "Can't parse object that contains an invalid field: %s" % str(data)
        )

    try:
        OBJ_MAP = OPENC2_OBJ_MAPS[component_type]
        obj_class = OBJ_MAP[_type]
    except KeyError:
        # check for extension
        try:
            EXT_MAP = OPENC2_OBJ_MAPS["extensions"]
            if component_type == "properties" and ":" in _type:
                obj_class = EXT_MAP[component_type][_type.split(":")[0]]
            else:
                obj_class = EXT_MAP[component_type][_type]
        except KeyError:
            if allow_custom:
                obj_class = dict
            else:
                raise exceptions.CustomContentError(
                    "Can't parse unknown target/actuator type '%s'!" % _type
                )

    # extended targets
    if component_type == "targets" and ":" in _type:
        nsid, target = _type.split(":")
        obj = {target: obj[_type]}
        _type = target

    if isinstance(_specifiers, dict):
        obj = obj[_type]

    return (obj, obj_class, _type, nsid)


def _get_dict(data):
    """Return data as a dictionary.
    Input can be a dictionary, string, or file-like object.
    """

    if type(data) is dict:
        return data
    else:
        try:
            return json.loads(data)
        except TypeError:
            pass
        try:
            return json.load(data)
        except AttributeError:
            pass
        try:
            return dict(data)
        except (ValueError, TypeError):
            raise ValueError("Cannot convert '%s' to dictionary." % str(data))


def parse(data, allow_custom=False, version=None):
    # convert OpenC2 object to dict, if not already
    obj = _get_dict(data)
    # convert dict to full python-openc2 obj
    obj = dict_to_openc2(obj, allow_custom, version)

    return obj


def dict_to_openc2(openc2_dict, allow_custom=False, version=None):
    message_type = None
    if "action" in openc2_dict:
        message_type = "command"
    elif "status" in openc2_dict:
        message_type = "response"
    else:
        raise exceptions.ParseError(
            "Can't parse object that is not valid command or response: %s"
            % str(openc2_dict)
        )

    OBJ_MAP = OPENC2_OBJ_MAPS["objects"]
    try:
        obj_class = OBJ_MAP[message_type]
    except KeyError:
        if allow_custom:
            return openc2_dict
        raise exceptions.ParseError(
            "Can't parse unknown object type '%s'! For custom types, use the CustomObject decorator."
            % openc2_dict["type"]
        )

    return obj_class(allow_custom=allow_custom, **openc2_dict)


def parse_component(data, allow_custom=False, version=None, component_type=None):
    (obj, obj_class, _type, nsid) = _get_data_info(
        data, allow_custom=allow_custom, component_type=component_type
    )

    try:
        return obj_class(allow_custom=allow_custom, **obj)
    except:
        if component_type != "properties":
            parsed_obj = parse_component(
                data, allow_custom=allow_custom, component_type="properties",
            )

            sub_type = _type
            if nsid != _type:
                _type = "%s:%s" % (nsid, _type)

            return obj_class(**{sub_type: parsed_obj})
        raise


def parse_target(data, allow_custom=False, version=None):
    return parse_component(data, allow_custom, version, component_type="targets")


def parse_actuator(data, allow_custom=False, version=None):
    return parse_component(data, allow_custom, version, component_type="actuators")


def parse_args(data, allow_custom=False, version=None):
    dictified = copy.deepcopy(data)
    default_args = list(OPENC2_OBJ_MAPS["args"]["args"]._properties.keys())
    specific_type_map = OPENC2_OBJ_MAPS["extensions"]["args"]
    # iterate over each key and if its not in the default args, check extensions
    for key, subvalue in dictified.items():
        if key in default_args:
            continue
        # handle embedded custom args
        if key in specific_type_map:
            cls = specific_type_map[key]
            if type(subvalue) is dict:
                if allow_custom:
                    subvalue["allow_custom"] = True
                    dictified[key] = cls(**subvalue)
                else:
                    dictified[key] = cls(**subvalue)
            elif type(subvalue) is cls:
                # If already an instance of an _Extension class, assume it's valid
                dictified[key] = subvalue
            else:
                raise ValueError("Cannot determine extension type.")
        else:
            if allow_custom:
                dictified[key] = subvalue
            else:
                raise exceptions.CustomContentError(
                    "Can't parse unknown extension type: {}".format(key)
                )
    try:
        OBJ_MAP = OPENC2_OBJ_MAPS["args"]
        obj_class = OBJ_MAP["args"]
    except KeyError:
        raise exceptions.CustomContentError("Can't parse args '%s!" % data)

    return obj_class(allow_custom=allow_custom, **dictified)
