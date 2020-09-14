import config
import telebot
from gettext import gettext as _


class Mailer(telebot.TeleBot):
    admin_tg_id_list = config.ADMIN_TG_ID_LIST

    def send_free_space_warning(self, free_space: str,
                                current_backup_size: str,
                                min_backups_amount: int,
                                max_backups_amount: int):
        message = _("<b>Your backup space is running out!</b>"
                    "\nFree: <code>{free_space}</code>"
                    "\nCurrent backup size: <code>{current_backup_size}</code>"
                    "\nBackups amount: <code>from {min_backups_amount} to {max_backups_amount} backups.</code>"
                    "").format(free_space=free_space,
                               current_backup_size=current_backup_size,
                               min_backups_amount=min_backups_amount,
                               max_backups_amount=max_backups_amount)
        for tg_id in self.admin_tg_id_list:
            self.send_message(tg_id, message, parse_mode='html')

    def send_success_backup(self, db_name: str, backup_size: str):
        message = _("<b>Backup completed successfully!</b>\n"
                    "Data base: <code>{db_name}</code>\n"
                    "Backup size: <code>{backup_size}</code>"
                    "").format(db_name=db_name,
                               backup_size=backup_size)
        for tg_id in self.admin_tg_id_list:
            self.send_message(tg_id, message, parse_mode='html')

    def send_success_backup_with_warning(self, db_name: str, backup_size: str, previous_backup_size: str):
        message = _("<b>The backup is complete, but something went wrong!</b>\n"
                    "Data base: <code>{db_name}</code>\n"
                    "Backup size: <code>{backup_size}</code>\n"
                    "Previous backup size: <code>{previous_backup_size}</code>"
                    "").format(db_name=db_name,
                               backup_size=backup_size,
                               previous_backup_size=previous_backup_size)
        for tg_id in self.admin_tg_id_list:
            self.send_message(tg_id, message, parse_mode='html')

    def send_error(self, db_name: str):
        message = _("<b>Backup failed!</b>\n"
                    "Data base: <code>{db_name}</code>").format(db_name=db_name)
        for tg_id in self.admin_tg_id_list:
            self.send_message(tg_id, message, parse_mode='html')
