from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class DbAccessor:
    engine = create_engine('mysql+pymysql://root:Annieleo1!@localhost/BrokerBase', isolation_level = 'READ COMMITTED')

    def create_session(self):
        return Session(bind = DbAccessor.engine)
