
import sqlalchemy
from sqlalchemy import String, Column, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base




Base = declarative_base()

class Tanjian(Base):
    __tablename__ = 't_anjian'

    docid = Column('docid', String(36), primary_key=True)
    relate_id = Column(String(256))
    publish_date = Column(String(10))
    content_html = Column(sqlalchemy.UnicodeText())
    content = Column(sqlalchemy.UnicodeText())
    short_content = Column(sqlalchemy.UnicodeText())
    content_type = Column(Integer)
    content_date = Column(String(10))
    content_title = Column(String(256))
    content_progress = Column(String(256))
    content_num = Column(String(256))
    court_name = Column(String(128))
    



