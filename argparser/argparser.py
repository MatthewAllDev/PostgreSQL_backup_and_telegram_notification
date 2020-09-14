import argparse
from gettext import gettext as _
import os
import config
import gettext
import locale


class ArgParser:
    def __init__(self):
        parser = argparse.ArgumentParser(add_help=False)
        gettext.textdomain('PostgreSQL_backup')
        gettext.bindtextdomain('PostgreSQL_backup', './locale')
        parser.add_argument('-l', '--locale',
                            type=str,
                            choices=os.listdir('./locale'),
                            help=_('locale to use.'))
        args, _ignore = parser.parse_known_args()
        if args.locale:
            os.environ['LANG'] = args.locale
        else:
            try:
                if config.LOCALE and not config.LOCALE.isspace():
                    os.environ['LANG'] = config.LOCALE
                else:
                    raise AttributeError
            except AttributeError:
                _locale, _encoding = locale.getdefaultlocale()
                os.environ['LANG'] = _locale
        parser.add_argument('--help',
                            action='help',
                            default=argparse.SUPPRESS,
                            help=_('show this help message and exit.'))
        parser.add_argument('-v', '--version', action='version',
                            version='PostgreSQL backup + TG notification v1.0',
                            help=_('show program\'s version number and exit.'))
        parser.add_argument('-fsu', '--file_size_unit',
                            type=str,
                            choices='B, KB, MB, GB, TB'.split(', '),
                            help=_('file size units in notifications.'))
        parser.add_argument('-bi', '--backup_increase',
                            type=float,
                            help=_('increase the size of the backup file (in bytes)'
                                   '(necessary to predict the lack of free space).'))
        parser.add_argument('-h', '--pg_host',
                            type=str,
                            help=_('database server host or socket directory.'))
        parser.add_argument('-p', '--pg_port',
                            type=str,
                            help=_('database server port number.'))
        parser.add_argument('-U', '--pg_user',
                            type=str,
                            help=_('user to connect to the database.'))
        parser.add_argument('-P', '--pg_password',
                            type=str,
                            help=_('database user password.'))
        parser.add_argument('-do', '--pg_dump_options',
                            type=str,
                            help=_('additional backup options. see "pg_dump --help" for details.'))
        parser.add_argument('-bd', '--backup_dir',
                            type=str,
                            help=_('path to backup directory.'))
        parser.add_argument('-bfn', '--backup_file_name_pattern',
                            type=str,
                            help=_('pattern backup file name. '
                                   'must included {db_name} and {date}. '
                                   'example: "{db_name}_{date}.backup".'))
        parser.add_argument('-d', '--db_name',
                            type=str,
                            help=_('database to backup.'))
        parser.add_argument('-df', '--date_format',
                            type=str,
                            help=_('{date} format in backup file name. '
                                   'see '
                                   '"https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior"'
                                   ' for details.'))
        self.args = parser.parse_args()

    def get_parameters(self) -> dict:
        parameters = vars(self.args)
        parameters.pop('locale')
        return parameters
