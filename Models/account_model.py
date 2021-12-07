import os, pickle
from Database.accessor import DbAccessor
from cryptography.fernet import Fernet, InvalidToken
from Database.Entities.entities import Account

class AccountModel:
    def __init__(self):
        self.session = DbAccessor().create_session()

    def create(self, login, password, rolename):
        encrypted_password = self.encrypt_password(
            login,
            password
        )
        try:
            self.session.add(
                Account(
                    login = login, 
                    password = encrypted_password,
                    rolename = rolename
                )
            )
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error

    def delete(self, login):
        try:
            account = self.session.query(Account).filter(
                Account.login == login
            ).one()
            self.session.delete(account)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error

    def update(self, login, password, mob_num, email):
        encrypted_password = self.encrypt_password(
            login,
            password
        )
        try:
            if (account := self.session.query(Account).filter(
                    Account.login == login
                ).first()
            ):
                account.login = login
                account.password = encrypted_password
                account.mob_num = mob_num
                account.email = email
                self.session.commit()
            else:
                raise ValueError('account not found')
        except Exception as error:
            self.session.rollback()
            raise error

    def read(self):
        return self.session.query(
            Account.id,
            Account.login, 
            Account.password,
            Account.mob_num,
            Account.email,
            Account.rolename
        ).all()

    def dump_key(self, filename):
        key = Fernet.generate_key()
        file = open(filename, 'wb')
        pickle.dump(key, file)
        file.close()
        return key

    def load_key(self, filename):
        file = open(filename, 'rb')
        key = pickle.load(file)
        file.close()
        return key

    def encrypt_password(self, login, password):
        path = os.path.join('Database', 'AccKeys', login)
        if os.path.exists(path):
            key = self.load_key(path)
        else:
            key = self.dump_key(path)

        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, login, password):
        path = os.path.join('Database', 'AccKeys', login)
        key = self.load_key(path)
        cipher = Fernet(key)
        decrypted_password = cipher.decrypt(password.encode())
        return decrypted_password


