class ConfigOptionNotFoundException(Exception):
    """Raised when a necessary config option was not found in the config file.

    :param str option:
        The option that is missing.

    """
    def __init__(self, option):
        self.option = option

    def __repr__(self):
        return repr("The configuration option '{0}' was not found in the config file.".format(self.option))

class ConfigOptionInvalidException(Exception):
    """Raised when an invalid value is provided for an option in the config file.

    :param str option:
        The option in the config file.

    :param str value:
        The invalid value that was provided.

    """
    def __init__(self, option, value):
        self.option = option
        self.value = value

    def __repr__(self):
        return repr("The configuration option '{0}' has an invalid value of '{1}'".format(self.option, self.value))