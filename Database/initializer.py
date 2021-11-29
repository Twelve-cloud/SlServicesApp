from sqlalchemy import create_engine
from .Entities.entities import Base, Account, BanList, Company, Service, Basket, PriceHistory
from Logger.logger import Logger
from Database.accessor import DbAccessor

logger = Logger('logs', 'DbInitializer_loger.txt')
accessor = DbAccessor()

class DbInitializer:
    engine = create_engine('mysql+pymysql://root:Annieleo1!@localhost/BrokerBase', isolation_level = 'READ COMMITTED')

    def __init__(self, Base):
        self.Base = Base

    def create_tables(self):
        self.Base.metadata.create_all(DbInitializer.engine)

    def drop_tables(self):
        self.Base.metadata.drop_all(DbInitializer.engine)

    def create_triggers(self):
        try:
            DbInitializer.engine.execute('''CREATE TRIGGER autoupdatePrice_2 AFTER UPDATE ON Service
                                FOR EACH ROW BEGIN
                                    INSERT INTO PriceHistory(ServiceName, CompanyName, Price) VALUES (NEW.ServiceName, NEW.CompanyName, NEW.ServicePrice);
                                END'''
                        )
            DbInitializer.engine.execute('''CREATE TRIGGER autoupdatePrice AFTER INSERT ON Service
                                FOR EACH ROW BEGIN
                                    INSERT INTO PriceHistory(ServiceName, CompanyName, Price) VALUES (NEW.ServiceName, NEW.CompanyName, NEW.ServicePrice);
                                END'''
                        )
        except Exception as error:
            logger.write(f'Error with creating triggers: {error}')    

    def init_tables(self, log = False):
        try:
            session = accessor.create_session()
        
            session.add_all([
                Account(id = 1000, login = 'ur_god', password = 'god_pass', mob_num = '+375(99)999-99-99', email = 'godemail@god.ru', rolename = 'BROKER'),
                Company(company_name = 'Газпром'), 
                Company(company_name = 'Компания Ильи'),
                Service(service_name = 'Страховка газа', price = 999.99, company_name = 'Газпром'), 
                Service(service_name = 'Страховка нефти', price = 888.88, company_name = 'Газпром'), 
                Service(service_name = 'Страховка газа', price = 333.99, company_name = 'Компания Ильи'),
                Service(service_name = 'Страховка нефти', price = 222.88, company_name = 'Компания Ильи')]
            )
            session.commit()
        except Exception as error:
            logger.write(f'Error with initializing tables: {error}')  

    def clear_tables(self, log = False):
        try:
            session = accessor.create_session()
            session.query(Account).delete()
            session.query(BanList).delete()
            session.query(Company).delete()
            session.query(Service).delete()
            session.query(Basket).delete()
            session.query(PriceHistory).delete()
            session.commit()
        except Exception as error:
           logger.write(f'Error with clearing tables: {error}')  
