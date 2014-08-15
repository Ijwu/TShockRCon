from TShockRCon.exceptions import ConfigOptionNotFoundException
from configparser import ConfigParser
from os.path import exists

def get_config_value(value, category=None):
    """Get a value from the config.

    :param str value:
        The value to get from the config.

    :param str category:
        The section of the config to look in. Defaults to "SERVER".

    :returns: Value assigned to the config value.
    :rtype: str

    :raises ConfigOptionNotFoundException:
        If the config option is not found.

    """
    if category is None:
        try:
            return _config["SERVER"][value]
        except KeyError:
            raise ConfigOptionNotFoundException("SERVER."+value)
    else:
        try:
            return _config[category][value]
        except KeyError:
            raise ConfigOptionNotFoundException(category+"."+value)


def set_config_value():
    """I want config to be readonly. Let's avoid this if possible.
    Or just use another file for R/W config."""
    pass

def _create_default_config():
    default = ConfigParser()
    default.add_section("SERVER")
    x = "SERVER"
    default[x]["NAME"] = "Server_Name_Here"
    default[x]["IP"] = "localhost"
    default[x]["PORT"] = "7878"
    default[x]["SECRET_KEY"] = str(b"Sq\xe6\x12\xc8G\x86:.\xc6<\x9e\xf8\xac\xc7\xb4!{l\x98p\xf3\xdc\xe6\x9f\xa3\xd0\x16\x97'\xc12")
    return default

_config = ConfigParser()
if exists("config.ini"):
    _config.read("config.ini")
else:
    _config = _create_default_config()
    with open("config.ini", "w") as f:
        _config.write(f)