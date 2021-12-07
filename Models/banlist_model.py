import time
from Database.accessor import DbAccessor
from Database.Entities.entities import BanList

class BanListModel:
    def __init__(self):
        self.session = DbAccessor().create_session()
        self.bans = []

    def create(self, acc_id, started, ended):
        try:
            ban = BanList(
                    acc_id = acc_id, 
                    started = started,
                    ended = ended
                )
            self.session.add(ban)
            self.bans.append(ban)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error

    def delete(self, acc_id):
        try:
            ban = self.session.query(BanList).filter(
                BanList.acc_id == acc_id
            ).one()
            self.session.delete(ban)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error

    def update(self, acc_id, started, ended):
        try:
            if (ban := self.session.query(BanList).filter(
                    BanList.acc_id == acc_id
                ).first()
            ):
                ban.started = started
                ban.ended = ended
                self.session.commit()
            else:
                raise ValueError('account not found')
        except Exception as error:
            self.session.rollback()
            raise error

    def read(self):
        return self.session.query(
            BanList.id,
            BanList.acc_id, 
            BanList.started,
            BanList.ended
        ).all()

    def get_bans(self):
        return self.bans
