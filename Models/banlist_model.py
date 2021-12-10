import time
from Database.accessor import DbAccessor
from Database.Entities.entities import BanList

class BanListModel:
    def create(self, acc_id, started, ended):
        self.session = DbAccessor().create_session()
        try:
            ban = BanList(
                    acc_id = acc_id, 
                    started = started,
                    ended = ended
                )
            self.session.add(ban)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def delete(self, acc_id):
        self.session = DbAccessor().create_session()
        try:
            ban = self.session.query(BanList).filter(
                BanList.acc_id == acc_id
            ).one()
            self.session.delete(ban)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def update(self, acc_id, started, ended):
        self.session = DbAccessor().create_session()
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
        finally:
            self.session.close()

    def read(self):
        self.session = DbAccessor().create_session()
        bans = self.session.query(
            BanList.id,
            BanList.acc_id, 
            BanList.started,
            BanList.ended
        ).all()
        self.session.close()
        return bans


