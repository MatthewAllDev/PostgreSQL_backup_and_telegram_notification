# MAIN SETTINGS
LOCALE: str = ''
FILE_SIZE_UNIT: str = ''
FREE_SPACE_THRESHOLD: int = 0
BACKUP_INCREASE: float = 0 # in bytes

# POSTGRESQL CONNECTION SETTINGS
PG_HOST: str = ''
PG_PORT: str = ''
PG_USER: str = ''
PG_PASSWORD: str = ''
PG_DUMP_OPTIONS: str = ''

# BACKUP SETTINGS
PG_DUMP_PATH: str = ''
BACKUP_DIR: str = ''
BACKUP_FILE_NAME_PATTERN: str = ''  # must included {db_name} and {date}
DB_NAME: str = ''
DATE_FORMAT: str = ''

# MAILER SETTINGS
TG_TOKEN: str = ''
ADMIN_TG_ID_LIST: list = []
