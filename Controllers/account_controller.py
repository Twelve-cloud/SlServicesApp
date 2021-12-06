from Models.account_model import AccountModel
from Logger.logger import Logger
from Database.accessor import DbAccessor
from cryptography.fernet import Fernet
from Database.Entities.entities import Account
import os, pickle

logger = Logger('logs', 'account_controller_logs.txt')

class AccountController:
    def __init__(self, args):
        keys = [kv.split(':')[0] for kv in args]
        values = [kv.split(':')[1] for kv in args]
        self.kwargs = dict(zip(keys, values))
        self.model = AccountModel()
        self.session = DbAccessor().create_session()

    def register_account(self):
        try:
            self.model.create(**self.kwargs, rolename = 'USER')
            return 'REGISTRATION SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot add account to database, error: {error}')
            return 'REGISTRATION FAILED'

    def sign_in(self):
        try:
            login = self.kwargs['login']
            password = self.kwargs['password'] 
            
            path = os.path.join('Database', 'AccKeys', login)
            account_file = open(path, 'rb')
            cipher_key = pickle.load(account_file)
            account_file.close()

            cipher = Fernet(cipher_key)
            encrypted_password = cipher.encrypt(password.encode())

            if (account := self.session.query(Account).filter(
                    Account.login == login and  
                    Account.password == encrypted_password
                ).one()
            ):
                return 'AUTHENTIFICATION SUCCESSFUL~!#$~' + account.rolename
            else:
                return 'AUTHENTIFICATION FAILED'
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            return 'AUTHENTIFICATION FAILED'

    def get_information(self):
        try:
            login = self.kwargs['login']

            if (account := self.session.query(Account).filter(
                    Account.login == login
                ).one()
            ):
                path = os.path.join('Database', 'AccKeys', login)
                account_file = open(path, 'rb')
                cipher_key = pickle.load(account_file)
                account_file.close()

                cipher = Fernet(cipher_key)
                decrypted_password = cipher.decrypt(account.password.encode())
                print(account.password)
                print(decrypted_password)
                return f'{account.login}~!#$~{decrypted_password}~!#$~' \
                       f'{account.mob_num}~!#$~{account.email}'
            else:
                return 'GETDATA FAILED'
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







