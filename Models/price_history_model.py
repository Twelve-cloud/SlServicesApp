from Database.accessor import DbAccessor
from Database.Entities.entities import PriceHistory
from sqlalchemy import func

class PriceHistoryModel:
    def read(self):
        self.session = DbAccessor().create_session()
        phistory = self.session.query(
            PriceHistory.service_name,
            PriceHistory.company_name,
            PriceHistory.price
        ).all()
        self.session.close()
        return phistory

    def read_avg(self, service_name):
        self.session = DbAccessor().create_session()
        result = self.session.query(func.avg(PriceHistory.price).label('average'), 
                PriceHistory.company_name).filter(
                        PriceHistory.service_name == service_name
                ).group_by(PriceHistory.company_name
        ).all()
        self.session.close()
        return result

