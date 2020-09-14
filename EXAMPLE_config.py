# MAIN SETTINGS
LOCALE: str = 'en_US'
FILE_SIZE_UNIT: str = 'GB'
FREE_SPACE_THRESHOLD: int = 4
BACKUP_INCREASE: float = 200 * (1024 ** 2)  # in bytes

# POSTGRESQL CONNECTION SETTINGS
PG_HOST: str = '192.168.1.54'
PG_PORT: str = '5432'
PG_USER: str = 'Admin'
PG_PASSWORD: str = 'qwerty123456'
PG_DUMP_OPTIONS: str = '-F c -b -v'

# BACKUP SETTINGS
PG_DUMP_PATH: str = 'C:/Program Files/PostgreSQL/9.6.7-1.1C/bin/pg_dump'
BACKUP_DIR: str = 'B:/Backup'
BACKUP_FILE_NAME_PATTERN: str = '{db_name}_{date}.backup'  # must included {db_name} and {date}
DB_NAME: str = 'DB'
DATE_FORMAT: str = '%Y-%m-%d'

# MAILER SETTINGS
TG_TOKEN: str = 'TOKEN'
ADMIN_TG_ID_LIST: list = [132456, 987654]
