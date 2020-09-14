# PostgreSQL backup and telegram notification

This script intended to make and verifying PostgreSQL database backup and notification system administrators in telegram.
Script requires [Python](https://www.python.org/) v3 to run. (tested on v3.8 - Windows)

### Dependencies

* [telebot](https://pypi.org/project/pyTelegramBotAPI/) - A simple, but extensible Python implementation for the [Telegram Bot API](https://core.telegram.org/bots/api).
* [psutil](https://pypi.org/project/psutil/) - (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.

### How to use

1. Install modules [telebot](https://pypi.org/project/pyTelegramBotAPI/) and [psutil](https://pypi.org/project/psutil/).
2. Define in config.py: 
    * *PG_DUMP_PATH* 
    * *FREE_SPACE_THRESHOLD* 
    * *TG_TOKEN*
    * *ADMIN_TG_ID_LIST*
3. Run main.py with the required parameters. You can define persistent parameters in config.py.

**Attention!** Parameters passed at startup take precedence over parameters in config.py.

### Parameters
##### Only in config.py
* *PG_DUMP_PATH* - path to *pg_dump* utility on Windows / command to run this utility on * nix;
* *FREE_SPACE_THRESHOLD* - the threshold for the number of remaining backups to fit on disk at which administrators should be alerted;
* *TG_TOKEN* - telegram api token (you can take this in [@BotFather](tg://resolve?domain=BotFather));
* *ADMIN_TG_ID_LIST* - list of id of system administrators in Telegram (you can take you id in [@get_user_id_bot](tg://resolve?domain=get_user_id_bot)); 
##### At run or in config.py
* *LOCALE (-l, --locale)* - locale to use (optional parameter). Supported: en_US, ru_RU;
* *FILE_SIZE_UNIT (-fsu, --file_size_unit)* - file size units in notifications. Supported: B, KB, MB, GB, TB; 
* *BACKUP_INCREASE (-bi, --backup_increase)* - increase the size of the backup file (in bytes)(necessary to predict the lack of free space);
* *PG_HOST (-h, --pg_host)* - database server host or socket directory;
* *PG_PORT (-p, --pg_port)* - database server port number;
* *PG_USER (-U, --pg_user)* - user to connect to the database;
* *PG_PASSWORD (-P, --pg_password)* - database user password; 
* *PG_DUMP_OPTIONS (-do, --pg_dump_options)* - additional backup options. Example: "-F c -b -v". See "pg_dump --help" for details;
* *BACKUP_DIR (-bd, --backup_dir)* - path to backup directory;
* *BACKUP_FILE_NAME_PATTERN (-bfn, --backup_file_name_pattern)* -  pattern backup file name. Must included "{db_name}" and "{date}". Example: "{db_name}_{date}.backup";
* *DB_NAME (-d, --db_name)* - database to backup;
* *DATE_FORMAT (-df, --date_format)* - "{date}" format in backup file name. See [this](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior) for details.

**The repository has an example config.py (EXAMPLE_config.py)**

### How to execute this on schedule
##### Windows
1. Create task in "Task Scheduler";
2. As "Action" use "Start a program"; 
3. "Program/script" - path to python.exe; 
4. "Add arguments" - path to main.py and your parameters for the script;
5. "Start in (optional)" - path to the directory with main.py.