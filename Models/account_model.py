from Database.Entities.entities import Account
from Database.accessor import DbAccessor
from Logger.logger import Logger

logger = Logger('logs', 'account_model_logs.txt')

class AccountModel:
    def __init__(self, data):
        keys = [kv.split(':')[0] for kv in data]
        values = [kv.split(':')[1] for kv in data]
        self.data = dict(zip(keys, values))
        self.session = DbAccessor().create_session()

    def register(self):
        try:
            self.session.add(Account(**self.data))
            self.session.commit()
            return 'REGISTRATION SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot add account to database, error: {error}')
            return 'REGISTRATION FAILED'

    def sign_in(self):
        try:
            login, password = self.data
            if (account := self.session.query(Account).filter(Account.login == self.data[login] and Account.password == self.data[password]).one()):
                return 'AUTHENTIFICATION SUCCESSFUL~!#$~' + account.rolename
            else:
                return 'AUTHENTIFICATION FAILED'
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            return 'AUTHENTIFICATION FAILED'

    def get_info(self):
        try:
            login, password = self.data
            if (account := self.session.query(Account).filter(Account.login == self.data[login] and Account.password == self.data[password]).one()):
                return f'{account.login}~!#$~{account.password}~!#$~{account.mob_num}~!#$~{account.email}'
            else:
                return 'GETDATA FAILED'
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            return 'GETDATA FAILED'

    def redo_info(self):
        try:
            login, password, mob, email = self.data
            print(self.data)
            if (account := self.session.query(Account).filter(Account.login == self.data[login] and Account.password == self.data[password]).first()):
                account.login = self.data[login]
                account.password = self.data[password]
                account.mob_num = self.data[mob]
                account.email = self.data[email]
                self.session.commit()
                return 'REDO ACC INFO SUCCESS'
            else:
                return 'REDO ACC INFO FAILED'
        except Exception as error:
            logger.write(f'Cannot redo account info, error: {error}')
            return 'REDO ACC INFO FAILED'

    def delete(self):
        try:
            login, password = self.data 
            account = self.session.query(Account).filter(Account.login == self.data[login] and Account.password == self.data[password]).one()
            self.session.delete(account)
            self.session.commit()
            return 'DELETING SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot delete account, error: {error}')
            return 'DELETING FAILED'


