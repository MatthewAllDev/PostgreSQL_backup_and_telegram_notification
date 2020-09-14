from backup_manager import BackupManager
from argparser import ArgParser

if __name__ == '__main__':
    ap = ArgParser()
    backup_manager = BackupManager(**ap.get_parameters())
    backup_manager.check_free_space()
    if not backup_manager.is_actual_backup_exist():
        backup_manager.create_backup()
        backup_manager.check_actual_backup()
    else:
        backup_manager.check_actual_backup()
