from gettext import gettext as _


class ConfigurationException(Exception):
    def __init__(self, attr: str, config_only: bool = False):
        self.attr: str = attr
        self.config_only: bool = config_only

    def __str__(self):
        if self.config_only:
            txt = _('Parameter "{attr}" must be defined in config.py.').format(attr=self.attr)
        else:
            txt = _('Parameter "{attr}" must be defined in config.py '
                    'or in arguments when instantiating a class.').format(attr=self.attr)
        return txt
