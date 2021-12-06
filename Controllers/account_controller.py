from Models.account_model import AccountModel
from Logger.logger import Logger

logger = Logger('logs', 'account_controller_logs.txt')

class AccountController:
    def __init__(self, args):
        keys = [kv.split(':')[0] for kv in args]
        values = [kv.split(':')[1] for kv in args]
        self.kwargs = dict(zip(keys, values))
        self.model = AccountModel()

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
                decrypted_password = self.model.decrypt_password(account.login, account.password)
                if account.login == self.kwargs['login'] and \
                decrypted_password.decode() == self.kwargs['password']:
                    break
            else:
                return 'AUTHENTIFICATION FAILED'
            return 'AUTHENTIFICATION SUCCESSFUL~!#$~' + account.rolename
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            return 'AUTHENTIFICATION FAILED'

    def get_information(self):
        try:
            accounts = self.model.read()

            for account in accounts:
                if account.login == self.kwargs['login']:
                    break
            else:
                return 'GETDATA FAILED'
            decrypted_password = self.model.decrypt_password(
                account.login, account.password
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









