from Database.Entities.entities import Account
from Database.accessor import DbAccessor
from Logger.logger import Logger

logger = Logger('logs', 'account_model_logs.txt')

class AccountModel:
    def __init__(self, data):
        keys = [kv.split()[0] for kv in data]
        values = [kv.split()[0] for kv in data]
        self.data = dict(zip(keys, values))
        self.session = DbAccessor().create_session()

    def register(self):
        try:
            self.session.add(Account(**self.data))
            self.session.commit()
            return 'REGISTER SUCCESSFUL'
        except Exception as error:
            logger.write(f'Cannot add account to database, error: {error}')
            return 'REGISTER FAILED'

    def sign_in(self):
        try:
            login, password = self.data
            if self.session.query(Account).filter(Account.login == self.data[login] and Account.password == self.data[password]).one():
                return 'SIGN IN SUCCESSFUL'
            else:
                return 'SIGN IN FAILED'
        except Exception as error:
            logger.write(f'Cannot select account from database, error: {error}')
            return 'SIGN IN FAILED'

    def redo_info(self, data):
        login, password, mob, email = data
        account = self.session.query(Account).filter(Account.login == login and Account.password == password).one()

        if login != ' ': account.login == login
        if password != ' ': account.password == password
        if mob != ' ': account.mob_num = mob
        if email != ' ': account.email = email
        
        try:
            self.session.add(Account(*data))
            self.session.commit()
            return 'REGISTER SUCCESSFUL'
        except Exception:
            return 'REGISTER FAILED'

    def delete(self, data):
        login, password = data
        account = session.query(Account).filter(Account.login == login and Account.password == password).one()

        try:
            session.delete(account)
            session.commit()
            return 'DELETING SUCCESSFUL'
        except Exception:
            return 'DELETING FAILED'

