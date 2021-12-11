import time
from Models.banlist_model import BanListModel
from Controllers.account_controller import AccountController
from Logger.logger import Logger
from Database.Entities.entities import BanList

logger = Logger('logs', 'banlist_controller_logs.txt')

class BanListController:
    def __init__(self):
        self.model = BanListModel()
        self.account_controller = AccountController()

    def set_kwargs(self, **kwargs):
        self.kwargs = kwargs

    def ban_account(self):
        try:
            login = self.kwargs.pop('login')
            self.account_controller.set_kwargs(login = login)
            acc_id = self.account_controller.get_id_by_login()
            if not self.kwargs['started']:
                self.kwargs['started'] = time.strftime('%Y-%m-%d %H:%M:%S')
            self.model.create(acc_id, **self.kwargs)
            return 'BAN ACCOUNT SUCCESS'
        except Exception as error:
            logger.write(f'Cannot add ban to account, error: {error}')
            return 'BAN ACCOUNT FAILED' 

    def unban_account(self):
        try:
            login = self.kwargs.pop('login')
            self.account_controller.set_kwargs(login = login)
            acc_id = self.account_controller.get_id_by_login()
            self.model.delete(acc_id)
            return 'UNBAN ACCOUNT SUCCESS'
        except Exception:
            logger.write(f'Cannot delete account ban, error: {error}')
            return 'UNBAN ACCOUNT FAILED'

    def change_account_ban(self):
        try:
            login = self.kwargs.pop('login')
            self.account_controller.set_kwargs(login = login)
            acc_id = self.account_controller.get_id_by_login()
            if not self.kwargs['started']:
                self.kwargs['started'] = time.strftime('%Y-%m-%d %H:%M:%S')
            self.model.update(acc_id, **self.kwargs)
            return 'BAN ACCOUNT SUCCESS' 
        except Exception:
            logger.write(f'Cannot change account ban, error: {error}')
            return 'CHANGE ACCOUNT BAN FAILED'

    def view_all_bans(self):
        try:
            bans = self.model.read()
            print(
                '-' * 87, '|{:^6}|{:^24}|{:^26}|{:^26}|'.format(
                    'ID', 'ACC_ID', 'STARTED', 'ENDED'),
                '-' * 87, sep = '\n'
            )
            for ban in bans:
                self.account_controller.set_kwargs(id = ban.acc_id)
                login = self.account_controller.get_login_by_id()
                print(
                    '|{:^6}|{:^6}[{:^16}]|{:^26}|{:^26}|'.format(
                        ban.id, ban.acc_id, login, str(ban.started), str(ban.ended))
                )
            print('-' * 87)
        except Exception as error:
            logger.write(f'Cannot select ban from database, error: {error}')
            print('CANNOT READ DATA FROM DATABASE')

