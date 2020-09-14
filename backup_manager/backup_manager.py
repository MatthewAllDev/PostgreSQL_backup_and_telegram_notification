import config
import psutil
import datetime
import os
import re
from mailer import Mailer
from .exceptions import ConfigurationException
import math


class BackupManager:
    def __init__(self,
                 file_size_unit: str = None,
                 backup_increase: float = None,
                 pg_host: str = None,
                 pg_port: str = None,
                 pg_user: str = None,
                 pg_password: str = None,
                 pg_dump_options: str = None,
                 backup_dir: str = None,
                 backup_file_name_pattern: str = None,
                 db_name: str = None,
                 date_format: str = None):
        try:
            self.file_size_unit: str = file_size_unit if file_size_unit else config.FILE_SIZE_UNIT
        except AttributeError:
            self.file_size_unit = None
        try:
            self.backup_increase: float = backup_increase if backup_increase else config.BACKUP_INCREASE
        except AttributeError:
            self.backup_increase = None
        try:
            self.pg_host: str = pg_host if pg_host else config.PG_HOST
        except AttributeError:
            self.pg_host = None
        try:
            self.pg_port: str = pg_port if pg_port else config.PG_PORT
        except AttributeError:
            self.pg_port = None
        try:
            self.pg_user: str = pg_user if pg_user else config.PG_USER
        except AttributeError:
            self.pg_user = None
        try:
            self.pg_password: str = pg_password if pg_password else config.PG_PASSWORD
        except AttributeError:
            self.pg_password = None
        try:
            self.pg_dump_options: str = pg_dump_options if pg_dump_options else config.PG_DUMP_OPTIONS
        except AttributeError:
            self.pg_dump_options = None
        try:
            self.backup_dir: str = backup_dir if backup_dir else config.BACKUP_DIR
        except AttributeError:
            self.backup_dir = None
        try:
            self.backup_file_name_pattern: str = backup_file_name_pattern if backup_file_name_pattern else \
                config.BACKUP_FILE_NAME_PATTERN
        except AttributeError:
            self.backup_file_name_pattern = None
        try:
            self.db_name: str = db_name if db_name else config.DB_NAME
        except AttributeError:
            self.db_name = None
        try:
            self.date_format: str = date_format if date_format else config.DATE_FORMAT
        except AttributeError:
            self.date_format = None
        try:
            self.free_space_threshold: int = config.FREE_SPACE_THRESHOLD
        except AttributeError:
            self.free_space_threshold = None
        try:
            self.pg_dump_path: str = config.PG_DUMP_PATH
        except AttributeError:
            self.pg_dump_path = None
        try:
            self.tg_token: str = config.TG_TOKEN
        except AttributeError:
            self.tg_token = None
        try:
            self.admin_tg_id_list: list = config.ADMIN_TG_ID_LIST
        except AttributeError:
            self.admin_tg_id_list = None
        self.__check_configuration()
        self.free_space: float = psutil.disk_usage(self.backup_dir).free
        self.current_date: datetime.date = datetime.datetime.now().date()
        self.backups: list = os.listdir(self.backup_dir)
        self.last_backup_size: float = self.__get_last_backup_size()
        self.mailer: Mailer = Mailer(self.tg_token)
        self.actual_backup_filename: str = self.backup_file_name_pattern.format(db_name=self.db_name,
                                                                                date=self.current_date.strftime(
                                                                                    self.date_format))

    def check_free_space(self):
        min_amount: int = self.__get_min_copy_amount()
        if min_amount < self.free_space_threshold:
            max_amount = math.floor(self.free_space / self.last_backup_size)
            self.mailer.send_free_space_warning(self.convert_file_size(self.free_space),
                                                self.convert_file_size(self.last_backup_size),
                                                min_amount,
                                                max_amount)

    def is_actual_backup_exist(self) -> bool:
        return bool(self.backups.count(self.actual_backup_filename))

    def check_actual_backup(self):
        if not self.is_actual_backup_exist():
            self.mailer.send_error(self.db_name)
        else:
            backup_size = os.path.getsize(f'{self.backup_dir}/{self.actual_backup_filename}')
            if backup_size >= self.last_backup_size:
                self.mailer.send_success_backup(self.db_name, self.convert_file_size(backup_size))
            else:
                self.mailer.send_success_backup_with_warning(self.db_name,
                                                             self.convert_file_size(backup_size),
                                                             self.convert_file_size(self.last_backup_size))

    def create_backup(self):
        backup_path = f'{self.backup_dir}/{self.actual_backup_filename}'
        os.putenv('PGPASSWORD', self.pg_password)
        os.system(f'{self.pg_dump_path} -h {self.pg_host} -p {self.pg_port} -U {self.pg_user} '
                  f'{self.pg_dump_options} -f {backup_path} {self.db_name}')

    def __get_last_backup_size(self) -> float:
        pattern: str = self.backup_file_name_pattern.replace('{date}', '.*').format(db_name=self.db_name)
        backups: list = list(filter(lambda lst: re.match(pattern, lst), self.backups))
        last_backup_timestamp: float = 0
        last_backup_size: float = 0
        for backup in backups:
            backup_date = os.path.getmtime(f'{self.backup_dir}/{backup}')
            if (last_backup_timestamp < backup_date) and \
                    (datetime.datetime.fromtimestamp(backup_date).date() != self.current_date):
                last_backup_timestamp = backup_date
                last_backup_size = os.path.getsize(f'{self.backup_dir}/{backup}')
        return last_backup_size

    def __get_min_copy_amount(self) -> int:
        free_space = self.free_space
        last_backup_size = self.last_backup_size
        count = 0
        while free_space > last_backup_size:
            count += 1
            free_space -= last_backup_size
            last_backup_size += self.backup_increase
        return count

    def convert_file_size(self, number: float) -> str:
        units: dict = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 ** 4}
        val: float = round(number / (units.get(self.file_size_unit.upper())), 3)
        return '{0:,}'.format(val).replace(',', ' ') + f' {self.file_size_unit.upper()}'

    def __check_configuration(self):
        if not self.file_size_unit or self.file_size_unit.isspace():
            raise ConfigurationException('file_size_unit')
        if not self.backup_increase:
            raise ConfigurationException('backup_increase')
        if not self.pg_host or self.pg_host.isspace():
            raise ConfigurationException('pg_host')
        if not self.pg_port or self.pg_port.isspace():
            raise ConfigurationException('pg_port')
        if not self.pg_user or self.pg_user.isspace():
            raise ConfigurationException('pg_user')
        if not self.pg_password or self.pg_password.isspace():
            raise ConfigurationException('pg_password')
        if self.pg_dump_options is None:
            raise ConfigurationException('pg_dump_options')
        if not self.backup_dir or self.backup_dir.isspace():
            raise ConfigurationException('backup_dir')
        if not self.backup_file_name_pattern or self.backup_file_name_pattern.isspace():
            raise ConfigurationException('backup_file_name_pattern')
        if not self.db_name or self.db_name.isspace():
            raise ConfigurationException('db_name')
        if not self.date_format or self.date_format.isspace():
            raise ConfigurationException('date_format')
        if self.free_space_threshold is None:
            raise ConfigurationException('free_space_threshold', True)
        if not self.pg_dump_path or self.pg_dump_path.isspace():
            raise ConfigurationException('pg_dump_path', True)
        if not self.tg_token or self.tg_token.isspace():
            raise ConfigurationException('tg_token', True)
        if not self.admin_tg_id_list:
            raise ConfigurationException('admin_tg_id_list', True)
