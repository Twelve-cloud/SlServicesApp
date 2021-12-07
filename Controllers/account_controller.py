import time
from Models.account_model import AccountModel
from Logger.logger import Logger
from Models.banlist_model import BanListModel

logger = Logger('logs', 'account_controller_logs.txt')

class AccountController:
    def __init__(self, args = None):
        if args:
            keys = [kv.split(':')[0] for kv in args]
            values = [kv.split(':')[1] for kv in args]
            self.kwargs = dict(zip(keys, values))
        self.model = AccountModel()
        self.ban_model = BanListModel()

    def set_kwargs(self, **kwargs):
        self.kwargs = kwargs

    def register_account(self):
        try:
            self.model.create(**self.kwargs, rolename = 'USER')
            return 'REGISTRATION SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot add account to database, error: {error}')
            return 'REGISTRATION FAILED'

    def sign_in(self):
        try:
            accounts = self.model.read()
            
            for account in accounts:
                decrypted_password = self.model.decrypt_password(
                    account.login, 
                    account.password
                )
                if account.login == self.kwargs['login'] and \
                decrypted_password.decode() == self.kwargs['password']:
                    break
            else:
                return 'AUTHENTIFICATION FAILED~!#$~Неверный логин или пароль'

            bans = self.ban_model.read()

            for ban in bans:
                if ban.acc_id == account.id:
                    break
            else:
                return 'AUTHENTIFICATION SUCCESSFUL~!#$~' + account.rolename
            
            if str(ban.ended) > time.strftime('%Y-%m-%d %H:%M:%S'):
                return 'AUTHENTIFICATION FAILED~!#$~Вы забанены до ' + str(ban.ended)
            else:
                self.ban_model.delete(account.id)
                return 'AUTHENTIFICATION SUCCESSFUL~!#$~' + account.rolename
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            return 'AUTHENTIFICATION FAILED~!#$~Неверный логин или пароль'

    def get_information(self):
        try:
            accounts = self.model.read()

            for account in accounts:
                if account.login == self.kwargs['login']:
                    break
            else:
                return 'GETDATA FAILED'
            decrypted_password = self.model.decrypt_password(
                account.login,
                account.password
            )
            return f'{account.login}~!#$~{decrypted_password.decode()}~!#$~' \
                   f'{account.mob_num}~!#$~{account.email}'
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            return 'GETDATA FAILED'


    def edit_information(self):
        try:
            self.model.update(**self.kwargs)
            return 'REDO ACC INFO SUCCESS'
        except Exception as error:
            logger.write(f'Cannot redo account info, error: {error}')
            return 'REDO ACC INFO FAILED'

    def delete_account(self):
        try:
            self.model.delete(**self.kwargs)
            return 'DELETING SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot delete account, error: {error}')
            return 'DELETING FAILED'

    def add_stuff_account(self):
        try:
            self.model.create(**self.kwargs)
            return 'REGISTRATION SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot create account, error: {error}')
            return 'REGISTRATION FAILED' 

    def view_all_accounts(self):
        try:
            accs = self.model.read()
            print(
                '-' * 122, '|{:^6}|{:^20}|{:^20}|{:^20}|{:^33}|{:^16}|'.format(
                    'ID', 'LOGIN', 'PASSWORD', 'MOBILE', 'EMAIL', 'ROLENAME'),
                '-' * 122, sep = '\n'
            )
            for acc in accs:
                print(
                    '|{:^6}|{:^20}|{:^20}|{:^20}|{:^33}|{:^16}|'.format(
                        acc.id, acc.login, '', acc.mob_num, acc.email, acc.rolename)
                )
            print('-' * 122)
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            print('CANNOT READ DATA FROM DATABASE') 

    def get_id_by_login(self):
        try:
            accs = self.model.read()
            for acc in accs:
                if acc.login == self.kwargs['login']:
                    return acc.id
            return 'ACCOUNT NOT EXIST'
        except Exception as error:
            logger.write(f'Cannot get id account by login from database, error: {error}')
            return 'ACCOUNT NOT EXIST'

    def get_login_by_id(self):
        try:
            accs = self.model.read()
            for acc in accs:
                if acc.id == self.kwargs['id']:
                    return acc.login
            return 'ACCOUNT NOT EXIST'
        except Exception as error:
            logger.write(f'Cannot get login account by id from database, error: {error}')
            return 'ACCOUNT NOT EXIST'






