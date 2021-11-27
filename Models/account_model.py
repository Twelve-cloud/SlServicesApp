class AccountModel:
    def __init__(self):
        self.session = None

    def register(self, data):
        try:
            self.session.add(Account(*data))
            self.session.commit()
            return 'REGISTER SUCCESSFUL'
        except Exception:
            return 'REGISTER FAILED'

    def sign_in(self, data):
        login, password = *data
        if self.session.query(Account).filter(Account.login == login and Account.password == password).one():
            return 'SIGN IN SUCCESSFUL'
        else
            return 'SIGN IN FAILED'

    def redo_info(self, data):
        login, password, mob, email = *data
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
        login, password = *data
        account = session.query(Account).filter(Account.login == login and Account.password == password).one()

        try:
            session.delete(account)
            session.commit()
            return 'DELETING SUCCESSFUL'
        except Exception:
            return 'DELETING FAILED'
