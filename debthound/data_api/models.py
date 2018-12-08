from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy import (Column, Integer, String, VARCHAR, DECIMAL, Date,
                        DateTime, JSON, Index, BOOLEAN, TIME)
from sqlalchemy import ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
import datetime


Base = declarative_base()
Deferred_Base = declarative_base(DeferredReflection)


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'mysql')
def ms_utcnow(element, compiler, **kw):
    return "CURRENT_TIMESTAMP"


class AuthType(Base):
    __tablename__ = 'authtype'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    sites = relationship('Site', backref="authtype")


sitedoctype_asoc = Table('sitedoctype_association', Base.metadata,
                    Column('site_id', Integer, ForeignKey('site.id')),
                    Column('doctype_id', Integer, ForeignKey('sitedoctype.id')))


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    base_url = Column(String(200))
    last_scrape_datetime = Column(DateTime, nullable=False, default=datetime.datetime.min)
    creds = Column(JSON)
    auth_type_id = Column(Integer, ForeignKey('authtype.id'))
    doctypes = relationship("SiteDocType", secondary=sitedoctype_asoc, backref='sites')
    scrape_logs = relationship('SiteScrapeLog', back_populates='site')
    spider_name = Column(String(50), nullable=False)
    schedules = relationship('Schedule', back_populates='site')
    last_poll_datetime = Column(DateTime, nullable=False, default=datetime.datetime.min)


class SiteDocType(Base):
    __tablename__ = 'sitedoctype'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50))


class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    book = Column(String(100))
    book_type = Column(String(50))
    cfn = Column(String(250))
    consideration = Column(DECIMAL(12, 2))
    cross_name = Column(VARCHAR(500))
    date = Column(Date)
    image_uri = Column(VARCHAR(800))
    legal = Column(String(200))
    name = Column(String(200))
    page = Column(String(50))
    pages = Integer
    party1 = Column(VARCHAR(1500))
    party2 = Column(VARCHAR(1500))
    doctype_id = Column(Integer, ForeignKey(SiteDocType.id), nullable=False)
    doc_type = relationship(SiteDocType, backref='documents')
    site_id = Column(Integer, ForeignKey('site.id'), nullable=False)
    site = relationship(Site)
    flags = relationship('DocumentFlag', secondary='documentflag_association', backref='documents')
    info = Column('info', VARCHAR(1000))


Index('party1', Document.party1, mysql_length=100)
Index('party2', Document.party2, mysql_length=100)
Index('date', Document.date)
Index('cfn', Document.cfn, unique=True)


class DocumentFlag(Base):
    __tablename__ = 'documentflag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50))


Table('documentflag_association', Base.metadata,
      Column('document_id', Integer, ForeignKey(Document.id)),
      Column('documentflag_id', Integer, ForeignKey(DocumentFlag.id)))


class SiteScrapeLog(Base):
    __tablename__ = 'sitescrapelog'
    id = Column('id', Integer, primary_key=True)
    start_datetime = Column('start_datetime', DateTime, nullable=False)
    end_datetime = Column('end_datetime', DateTime)
    params = Column('params', VARCHAR(500))
    error = Column('error', VARCHAR(5000))
    site_id = Column('site_id', Integer, ForeignKey(Site.id), nullable=False)
    site = relationship(Site, back_populates='scrape_logs')
    log_details = relationship('SiteScrapeLogDetails', back_populates='site_scrape_log')


class SiteScrapeLogDetails(Base):
    __tablename__ = 'sitescrapelogdetails'
    id = Column('id', Integer, primary_key=True)
    site_scrape_log_id = Column('site_scrape_log_id', Integer, ForeignKey(SiteScrapeLog.id), nullable=False)
    site_scrape_log = relationship(SiteScrapeLog, back_populates='log_details')
    message = Column('message', VARCHAR(1000), nullable=False)
    info = Column('info', VARCHAR(1000))
    time_stamp = Column('time_stamp', DateTime, server_default=utcnow())


class Entity(Base):
    __tablename__ = 'entity'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR(1500), nullable=False)
    document_facts = relationship('DocumentFact', back_populates='entity')
    flags = relationship('EntityFlag', secondary='entity_flag_association', enable_typechecks=False)


class EntityFlag(Base):
    __tablename__ = 'entityflag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50))


Table('entity_flag_association', Base.metadata,
      Column('entity_id', Integer, ForeignKey(Entity.id)),
      Column('entity_flag_id', Integer, ForeignKey(EntityFlag.id)))


Index('idx_name', Entity.name, mysql_length=100)


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    day = Column(Integer, nullable=False)
    exact = Column(BOOLEAN, nullable=False)
    time = Column(TIME, nullable=False)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)
    site_id = Column(Integer, ForeignKey(Site.id))
    site = relationship(Site, back_populates='schedules')


class DocumentFact(Base):
    __tablename__ = 'documentfact'
    id = Column('id', Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey(Document.id), nullable=False)
    document = relationship(Document)
    entity_id = Column(Integer, ForeignKey(Entity.id), nullable=False)
    entity = relationship(Entity, back_populates='document_facts')


class ETL(DeferredReflection):
    __tablename__ = 'work_document_etl'


class SessionContext:
    def __init__(self, url, logger=None):
        self.engine = create_engine(url)
        self.session = None
        self.logger = None

    def __enter__(self):
        self.session = sessionmaker(self.engine)()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
            if self.logger:
                self.logger.exception(exc_val)
        self.session.close()


def get_scoped(url):
    eng = create_engine(url)
    s = scoped_session(sessionmaker(bind=eng))
    return s
