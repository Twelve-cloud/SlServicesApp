import time
from Database.accessor import DbAccessor
from Database.Entities.entities import BanList

class BanListModel:
    def __init__(self):
        self.session = DbAccessor().create_session()

    def create(self, acc_id, ended, started = None):
        if started:
            self.session.add(
                BanList(
                    acc_id = acc_id, 
                    started = started,
                    ended = ended
                )
            )
        else:
           self.session.add(
                BanList(
                    acc_id = acc_id, 
                    ended = ended
                )
            ) 
        self.session.commit()

    def delete(self, acc_id):
        ban = self.session.query(BanList).filter(
            BanList.acc_id == acc_id
        ).one()
        self.session.delete(ban)
        self.session.commit()

    def update(self, acc_id, ended, started = None):
        if (ban := self.session.query(BanList).filter(
                BanList.acc_id == acc_id
            ).first()
        ):
            if started:
                ban.started = started
            else:
                ban.started = time.strftime('%Y-%m-%d %H:%M:%S')
            ban.ended = ended
        self.session.commit()

    def read(self):
        return self.session.query(
            BanList.id,
            BanList.acc_id, 
            BanList.started,
            BanList.ended
        ).all()