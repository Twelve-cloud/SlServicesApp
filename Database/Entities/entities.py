from sqlalchemy import Column, Integer, String, Date, CheckConstraint, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'Account'
    
    id       = Column('ID', Integer, autoincrement = True, nullable = False, primary_key = True)
    login    = Column('AccountLogin', String(50), CheckConstraint(sqltext = "AccountLogin REGEXP '^[:alpha:][[:alnum:]_]{4,14}[:alnum:]$'", name = 'ch_login'), unique = True)
    password = Column('AccountPassword', String(50), CheckConstraint(sqltext = "AccountPassword REGEXP '^[:alnum:][[:alnum:]_]{4,30}[:alnum:]$'", name = 'ch_password'))
    mob_num  = Column('MobileNumber', String(50), CheckConstraint(sqltext = "MobileNumber REGEXP '^[+][:digit:]{3}[(][:digit:]{2}[)][:digit:]{3}-[:digit:]{2}-[:digit:]{2}$'", name = 'ch_mobnum'), unique = True, server_default = '+999(99)999-99-99')
    email    = Column('Email', String(50), CheckConstraint(sqltext = "Email REGEXP '^[:alpha:][[:alnum:]_]{5,15}[@][:alpha:]{2,10}[\.][:alpha:]{2,3}$'", name = 'ch_email'), unique = True, server_default = 'myemail@domen.com')
    rolename = Column('Rolename', String(50), CheckConstraint(sqltext = "Rolename IN ('BROKER', 'CONSULTANT', 'USER')", name = 'ch_rolename'), server_default = 'USER')

class BanList(Base):
    __tablename__  = 'BanList'

    id      = Column('ID', Integer, autoincrement = True, nullable = False, primary_key = True)
    acc_id  = Column('Account_ID', Integer, nullable = False, unique = True)
    started = Column('started', Date, nullable = False)
    ended   = Column('ended', Date, nullable = False)

    __table_args__ = (
        ForeignKeyConstraint(columns = ['Account_ID'], refcolumns = ['Account.ID'], ondelete = 'RESTRICT', onupdate = 'CASCADE', name = 'fkey_account'),
    )

class Company(Base):
    __tablename__ = 'Company'
    
    id           = Column('ID', Integer, nullable = False, primary_key = True)
    company_name = Column('CompanyName', String(50), CheckConstraint(sqltext = "CompanyName REGEXP '^[[:alnum:] \"]{6,16}$'", name = 'ch_cname'), unique = True)

class Service(Base):
    __tablename__ = 'Service'

    service_name = Column('ServiceName', String(50), CheckConstraint(sqltext = "ServiceName REGEXP '^[[:alnum:] \"]{6,32}$'", name = 'ch_sname'))
    price        = Column('ServicePrice', FLOAT(8, 2))
    company_name = Column('CompanyName', String(50))
    
    __table_args__ = (
        ForeignKeyConstraint(columns = ['CompanyName'], refcolumns = ['Company.CompanyName'], ondelete = 'CASCADE', onupdate = 'CASCADE', name = 'fkey_company'),
        PrimaryKeyConstraint('ServiceName', 'CompanyName', name = 'pkey_service')
    )
    
class Basket(Base):
    __tablename__ = 'Basket'

    id           = Column('AccountID', Integer())
    service_name = Column('ServiceName', String(50))

    __table_args__ = (
        ForeignKeyConstraint(columns = ['AccountID'], refcolumns = ['Account.ID'], ondelete = 'RESTRICT', onupdate = 'CASCADE', name = 'fkey_acc'),
        PrimaryKeyConstraint('AccountID', 'ServiceName', name = 'pkey_basket')
    )

class PriceHistory(Base):
    __tablename__ = 'PriceHistory'

    id           = Column('ID', Integer, nullable = False, primary_key = True) 
    service_name = Column('ServiceName', String(50))
    company_name = Column('CompanyName', String(50))
    price        = Column('Price', FLOAT(8,2), nullable = False)
    
    __table_args__ = (
        ForeignKeyConstraint(columns = ['ServiceName', 'CompanyName'], refcolumns = ['Service.ServiceName', 'Service.CompanyName'], ondelete = 'CASCADE', onupdate = 'CASCADE', name = 'fkey_sprice'),
    )
