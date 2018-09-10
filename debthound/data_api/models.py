from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, VARCHAR, DECIMAL, Date,
                        DateTime, JSON)
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship


Base = declarative_base()


class AuthType(Base):
    __tablename__ = 'authtype'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    sites = relationship('Site', backref="authtype")


sitedoctype_asoc = Table('sitedoctype_association', Base.metadata,
                    Column('site_id', Integer, ForeignKey('site.id')),
                    Column('doctype_id', Integer, ForeignKey('doctype.id')))


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    base_url = Column(String(200))
    last_scrape_datetime = Column(DateTime)
    creds = Column(JSON)
    auth_type_id = Column(Integer, ForeignKey('authtype.id'))
    doctypes = relationship("DocType", secondary=sitedoctype_asoc, backref='sites')


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
    name = String(200)
    page = Column(String(50))
    pages = Integer
    party1 = Column(VARCHAR(500))
    party2 = Column(VARCHAR(500))
    doctype_id = Column(Integer, ForeignKey(SiteDocType.id))
    doc_type = relationship(SiteDocType, backref='documents')
    site_id = Column(Integer, ForeignKey('site.id'))
    flags = relationship('DocumentFlag', secondary='documentflag_association',
                         backref='documents')


class DocumentFlag(Base):
    __tablename__ = 'documentflag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50))


Table('documentflag_association', Base.metadata,
      Column('document_id', Integer, ForeignKey(Document.id)),
      Column('documentflag_id', Integer, ForeignKey(DocumentFlag.id)))
