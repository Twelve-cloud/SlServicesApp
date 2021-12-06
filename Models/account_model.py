import os, pickle
from Database.Entities.entities import Account
from Database.accessor import DbAccessor
from Logger.logger import Logger
from cryptography.fernet import Fernet

logger = Logger('logs', 'account_model_logs.txt')

class AccountModel:
    def __init__(self, data):
        keys = [kv.split(':')[0] for kv in data]
        values = [kv.split(':')[1] for kv in data]
        self.data = dict(zip(keys, values))
        self.session = DbAccessor().create_session()

    def register(self):
        try:
            login = self.data['login']
            password = self.data['password']
            
            cipher_key = Fernet.generate_key()
            path = os.path.join('Database', 'AccKeys', login)
            account_file = open(path, 'wb')
            pickle.dump(cipher_key, account_file)
            account_file.close()

            cipher = Fernet(cipher_key)
            encrypted_password = cipher.encrypt(password.encode())
            print(password)

            self.session.add(Account(
                login = login, 
                password = encrypted_password)
            )
            self.session.commit()
            return 'REGISTRATION SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot add account to database, error: {error}')
            return 'REGISTRATION FAILED'

    def sign_in(self):
        try:
            login = self.data['login']
            password = self.data['password'] 
            
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

    def get_info(self):
        try:
            login = self.data['login']

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

    def redo_info(self):
        try:
            login = self.data['login']
            password = self.data['password']
            mob_num = self.data['mob_num']
            email = self.data['email']

            path = os.path.join('Database', 'AccKeys', login)
            account_file = open(path, 'rb')
            cipher_key = pickle.load(account_file)
            account_file.close()

            cipher = Fernet(cipher_key)
            encrypted_password = cipher.encrypt(password.encode())

            if (account := self.session.query(Account).filter(
                    Account.login == login
                ).first()
            ):
                account.login = login
                account.password = encrypted_password
                account.mob_num = mob_num
                account.email = email
                self.session.commit()
                return 'REDO ACC INFO SUCCESS'
            else:
                return 'REDO ACC INFO FAILED'
        except Exception as error:
            logger.write(f'Cannot redo account info, error: {error}')
            return 'REDO ACC INFO FAILED'

    def delete(self):
        try:
            login = self.data['login']
            account = self.session.query(Account).filter(
                Account.login == login
            ).one()
            self.session.delete(account)
            self.session.commit()
            return 'DELETING SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot delete account, error: {error}')
            return 'DELETING FAILED'


