
import jieba
from databaseMethod import Tanjian 
import sqlalchemy
from sqlalchemy import String, Column, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base

import judgement
import textAnalysis

print('hi')

engine=create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/wenshu_corruption?charset=utf8", max_overflow=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()
##anjian = session.query(Tanjian).filter(Tanjian.docid=='bf33e974-a358-4007-bbbb-9940bd9a5a3c').one()
##
##print(anjian.content_html)
##
##print('docid:', anjian.docid)
##print('publish_date:', anjian.publish_date)



anjian_list = session.query(Tanjian).filter(Tanjian.court_name == '广州市天河区人民法院').all()
for i,aj in enumerate(anjian_list):
    if i <= 0 :
        print(str(i),': docid:', aj.docid)
        cj = judgement.criminalJudgement(aj)
        #print(cj.content_html)
        print(cj.docid)
        #print(cj.paragraphs)
        for paragraph in cj.paragraphs:
            print(paragraph.no)
            print(paragraph.text)
            print(paragraph.ctype)
        #    print(jieba.lcut(paragraph))
        
        #for j in cj.litigant_list:
        #    print(j)

##
###
##print('docid:', anjian[0].docid)
##print('publish_date:', anjian[0].publish_date)
##print('content_date:', anjian[0].content_date)
##print('content_html:', anjian[0].content_html)
##
##session.close()

session.close()
