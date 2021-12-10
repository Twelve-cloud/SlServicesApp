from Database.accessor import DbAccessor
from Database.Entities.entities import Basket

class BasketModel:
    def create(self, acc_id, name, type):
        self.session = DbAccessor().create_session()
        try:
            if not self.session.query(Basket).get((acc_id, name)):
                basket = Basket(
                        acc_id = acc_id, 
                        name = name,
                        type = type,
                    )
                self.session.add(basket)
                self.session.commit()
            else:
                raise ValueError('BASKET EXISTS')
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def delete(self, acc_id, name):
        self.session = DbAccessor().create_session()
        try:
            if self.session.query(Basket).get((acc_id, name)):
                basket = self.session.query(Basket).filter(
                    Basket.acc_id == acc_id and
                    Basket.name == name
                ).one()
                self.session.delete(basket)
                self.session.commit()
            else:
                raise ValueError('BASKET NOT EXIST')
        except Exception as error:
            self.session.rollback()
            raise error
        finally:
            self.session.close()

    def read(self):
        self.session = DbAccessor().create_session()
        baskets = self.session.query(
            Basket.acc_id,
            Basket.name, 
            Basket.type,
            Basket.time
        ).all()
        self.session.close()
        return baskets
