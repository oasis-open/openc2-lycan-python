"""OpenC2 Error Classes."""


class OpenC2Error(Exception):
    """Base class for errors generated in the openc2 library."""


class ObjectConfigurationError(OpenC2Error):
    """
    Represents specification violations regarding the composition of OpenC2
    objects.
    """

    pass


class InvalidValueError(ObjectConfigurationError):
    """An invalid value was provided to a OpenC2 object's ``__init__``."""

    def __init__(self, cls, prop_name, reason):
        super(InvalidValueError, self).__init__()
        self.cls = cls
        self.prop_name = prop_name
        self.reason = reason

    def __str__(self):
        msg = "Invalid value for {0.cls.__name__} '{0.prop_name}': {0.reason}"
        return msg.format(self)


class PropertyPresenceError(ObjectConfigurationError):
    """
    Represents an invalid combination of properties on a OpenC2 object.  This
    class can be used directly when the object requirements are more
    complicated and none of the more specific exception subclasses apply.
    """

    def __init__(self, message, cls):
        super(PropertyPresenceError, self).__init__(message)
        self.cls = cls


class MissingPropertiesError(PropertyPresenceError):
    """Missing one or more required properties when constructing OpenC2 object."""

    def __init__(self, cls, properties):
        self.properties = sorted(properties)

        msg = "No values for required properties for {0}: ({1}).".format(
            cls.__name__, ", ".join(x for x in self.properties),
        )

        super(MissingPropertiesError, self).__init__(msg, cls)


class ExtraPropertiesError(PropertyPresenceError):
    """One or more extra properties were provided when constructing OpenC2 object."""

    def __init__(self, cls, properties):
        self.properties = sorted(properties)

        msg = "Unexpected properties for {0}: ({1}).".format(
            cls.__name__, ", ".join(x for x in self.properties),
        )

        super(ExtraPropertiesError, self).__init__(msg, cls)


class MutuallyExclusivePropertiesError(PropertyPresenceError):
    """Violating interproperty mutually exclusive constraint of a OpenC2 object type."""

    def __init__(self, cls, properties):
        self.properties = sorted(properties)

        msg = "The ({1}) properties for {0} are mutually exclusive.".format(
            cls.__name__, ", ".join(x for x in self.properties),
        )

        super(MutuallyExclusivePropertiesError, self).__init__(msg, cls)


class DependentPropertiesError(PropertyPresenceError):
    """Violating interproperty dependency constraint of a OpenC2 object type."""

    def __init__(self, cls, dependencies):
        self.dependencies = dependencies

        msg = "The property dependencies for {0}: ({1}) are not met.".format(
            cls.__name__, ", ".join(name for x in self.dependencies for name in x),
        )

        super(DependentPropertiesError, self).__init__(msg, cls)


class AtLeastOnePropertyError(PropertyPresenceError):
    """Violating a constraint of a OpenC2 object type that at least one of the given properties must be populated."""

    def __init__(self, cls, properties):
        self.properties = sorted(properties)

        msg = (
            "At least one of the ({1}) properties for {0} must be "
            "populated.".format(cls.__name__, ", ".join(x for x in self.properties),)
        )

        super(AtLeastOnePropertyError, self).__init__(msg, cls)


class DictionaryKeyError(ObjectConfigurationError):
    """Dictionary key does not conform to the correct format."""

    def __init__(self, key, reason):
        super(DictionaryKeyError, self).__init__()
        self.key = key
        self.reason = reason

    def __str__(self):
        msg = "Invalid dictionary key {0.key}: ({0.reason})."
        return msg.format(self)


class InvalidObjRefError(ObjectConfigurationError):
    """A OpenC2 Cyber Observable Object contains an invalid object reference."""

    def __init__(self, cls, prop_name, reason):
        super(InvalidObjRefError, self).__init__()
        self.cls = cls
        self.prop_name = prop_name
        self.reason = reason

    def __str__(self):
        msg = (
            "Invalid object reference for '{0.cls.__name__}:{0.prop_name}': {0.reason}"
        )
        return msg.format(self)


class InvalidSelectorError(ObjectConfigurationError):
    """Granular Marking selector violation. The selector must resolve into an existing OpenC2 object property."""

    def __init__(self, cls, key):
        super(InvalidSelectorError, self).__init__()
        self.cls = cls
        self.key = key

    def __str__(self):
        msg = "Selector {0} in {1} is not valid!"
        return msg.format(self.key, self.cls.__class__.__name__)


class TLPMarkingDefinitionError(ObjectConfigurationError):
    """Marking violation. The marking-definition for TLP MUST follow the mandated instances from the spec."""

    def __init__(self, user_obj, spec_obj):
        super(TLPMarkingDefinitionError, self).__init__()
        self.user_obj = user_obj
        self.spec_obj = spec_obj

    def __str__(self):
        msg = "Marking {0} does not match spec marking {1}!"
        return msg.format(self.user_obj, self.spec_obj)


class ImmutableError(OpenC2Error):
    """Attempted to modify an object after creation."""

    def __init__(self, cls, key):
        super(ImmutableError, self).__init__()
        self.cls = cls
        self.key = key

    def __str__(self):
        msg = "Cannot modify '{0.key}' property in '{0.cls.__name__}' after creation."
        return msg.format(self)


class UnmodifiablePropertyError(OpenC2Error):
    """Attempted to modify an unmodifiable property of object when creating a new version."""

    def __init__(self, unchangable_properties):
        super(UnmodifiablePropertyError, self).__init__()
        self.unchangable_properties = unchangable_properties

    def __str__(self):
        msg = "These properties cannot be changed when making a new version: {0}."
        return msg.format(", ".join(self.unchangable_properties))


class RevokeError(OpenC2Error):
    """Attempted an operation on a revoked object."""

    def __init__(self, called_by):
        super(RevokeError, self).__init__()
        self.called_by = called_by

    def __str__(self):
        if self.called_by == "revoke":
            return "Cannot revoke an already revoked object."
        else:
            return "Cannot create a new version of a revoked object."


class ParseError(OpenC2Error):
    """Could not parse object."""

    def __init__(self, msg):
        super(ParseError, self).__init__(msg)


class CustomContentError(OpenC2Error):
    """Custom OpenC2 Content (SDO, Observable, Extension, etc.) detected."""

    def __init__(self, msg):
        super(CustomContentError, self).__init__(msg)


class MarkingNotFoundError(OpenC2Error):
    """Marking violation. The marking reference must be present in SDO or SRO."""

    def __init__(self, cls, key):
        super(MarkingNotFoundError, self).__init__()
        self.cls = cls
        self.key = key

    def __str__(self):
        msg = "Marking {0} was not found in {1}!"
        return msg.format(self.key, self.cls.__class__.__name__)


class OpenC2DeprecationWarning(DeprecationWarning):
    """
    Represents usage of a deprecated component of a OpenC2 specification.
    """

    pass
