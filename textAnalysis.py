
import re
from bs4 import BeautifulSoup

from litigant import litigant



##def get_litigant_list(text): 
##    temp=[]
##    #提取被告人姓名
##    temp=temp+[get_info(text,r'^\s*被告人.*?[，。]|上诉人（?原审被告人）?.*?[，|。]')[-1]]
##    text=get_text(text,r'被告人.*?[，。]|上诉人（?原审被告人）?.*?[，|。]')
##    #提取被告人性别
##    temp=temp+[get_info(text,r'[男女][，。]')[0]]
##    text=get_text(text,r'[男女][，。]')
##    #提取生日
##    temp=temp+[get_info(text,r'生于[\d|X]{4}年.+?月.+?日|[\d|X]{4}年.+?月.+?日出?生')[-1]]
##    text=get_text(text,r'生于[\d|X]{4}年.+?月.+?日|[\d|X]{4}年.+?月.+?日出?生')
##    #提取逮捕时间等
##    temp=temp+get_treatment(text)
####    print("*"*100)
####    print("temp")
####    print(temp)
####    print("*"*100)
##    return temp

class paragraph(object):
    no = None
    text = None
    ctype = None
    
    

def paragraphing(content_html):
    paragraphs = []
    soup = BeautifulSoup(content_html, 'html.parser')
    for i, div in enumerate(soup.find_all('div')):
        para = paragraph()
        para.no = i
        para.text = div.string
        paragraphs.append(para)
    return paragraphs

def get_litigants_FI(paragraphs):
    for i, paragraph in enumerate(paragraphs):
        print(i, get_info(paragraph,r'^\s*被告人.*?[，。]|上诉人（?原审被告人）?.*?[，|。]')[-1])
        print(get_info(get_info(paragraph,r'^\s*被告人.*?[，。]|上诉人（?原审被告人）?.*?[，|。]')[-1],r'(?<=被告人).*?(?=[，。])')[0])
    

def get_litigant_list(document, docid):
    #print(document)
    li = litigant(docid)
    li.name = get_info(document,r'^\s*被告人.*?[，。]|上诉人（?原审被告人）?.*?[，|。]')[-1]
    print("li.name: ", li.name)
    

#抽象出一个传入正则表达式和文本，提取出信息
def  get_info(text,re_str):
    obj=re.compile(re_str)
    temp=obj.findall(text)
    if temp==[]:
        temp=['']
    return temp

#传入一个正则表达式和文本，消除在文本中找到的正则文本并返回文本
def  get_text(text,re_str):
    obj=re.compile(re_str)
    temp=obj.findall(text)
    if temp!=[]:
        index=text.find(temp[0])
        text=text[index+len(temp[0]):]
    else:
        return text
    return text

#传入一个时间列表，将里面的时间全部转化为日期
def change_date(time_list):
    for i in range(0,len(time_list)):
        try:
            if re.search(r'\d{4}年\d+月\d+日?',time_list[i]):
                continue
            elif re.search(r'同日|当日',time_list[i]):
                time_list[i]=time_list[i-1]
            elif re.search(r'\d{4}月\d+月\d+日?',time_list[i]):
                time_list[i]=time_list[i][0:4]+time_list[i][4].replace('月','年')+time_list[i][5:]
            elif re.search(r'[\u4e00-\u9fa5]年\d+月\d+日?',time_list[i]):
                time_list[i]=time_list[i-1][0:4]+time_list[i][1:]
            elif re.search(r'次日',time_list[i]):
                year,month,day=re.findall(r'\d+',time_list[i-1])
                date_new=datetime.date(int(year),int(month),int(day))
                time_list[i]=date_new+datetime.timedelta(days=1)
                year,month,day=re.findall(r'\d+',time_list[i].strftime('%Y-%m-%d'))
                time_list[i]=year+'年'+month+'月'+day+'日'
            elif re.search(r'[\u4e00-\u9fa5]月\d+日?',time_list[i]):
                year=re.findall(r'\d+',time_list[i-1])[0]
                month=str(int(re.findall(r'\d+',time_list[i-1])[1])+1)
                day=re.findall(r'\d+',time_list[i])[0]
                time_list[i]=year+'年'+month+'月'+day+'日'
            elif re.search(r'(?<![年\d])\d+月\d+日?',time_list[i]):
                year=re.findall(r'\d+',time_list[i-1])[0]
                month,day=re.findall(r'\d+',time_list[i])
                time_list[i]=year+'年'+month+'月'+day+'日'
            else:
                continue
        except:
            continue
    for i in range(0,len(time_list)):
        if re.search(r'\d{4}年\d+月\d+日?|',time_list[i]):
            continue
        else:
            print('日期有问题')
            break
    return time_list


#传入一个文本，来提取逮捕时间等信息
def get_treatment(text):
    temp=[]   #用于存储最后的时间和处理流程
    #用于存储要删除的索引
    time_list=[]
    treat_list=[]
    new_time=[]
    ti_index=0
    tr_index=0
    time_re=r'(?<!至)\d{4}年\d+月\d+日?(?!至)|\d{4}月\d+月\d+日?|[\u4e00-\u9fa5]年\d+月\d+日?|同日|当日|次日|(?<!（)现(?![暂居住])|[\u4e00-\u9fa5]月\d+日?|(?<![年\d])\d+月\d+日?|[\d|X]{4}年X月X日'
    treat_re=r'立案侦查|羁押|刑事拘留|(?<!执行)逮捕|(?<!决定)逮捕|取?保候审|在家|监视居住|决定逮捕|执行逮捕|批准逮捕|投案[自首]*|归案|传唤|取保侯审'
    temp1=re.findall(time_re,text)
    temp2=re.findall(treat_re,text)
    for t in temp1:
        new_time.append(t)
    new_time=change_date(new_time)
    if temp1==[] or temp2==[]:
        return temp
    while (len(temp1)-len(time_list))!=(len(temp2)-len(treat_list)):
        if (len(temp1)-len(time_list))>(len(temp2)-len(treat_list)):
            if text.find(temp1[ti_index])>text.find(temp2[tr_index]):
              #      print('1')
                treat_list.append(tr_index)
                text=get_text(text,temp2[tr_index])
                tr_index=tr_index+1
                if tr_index==len(temp2):
                    while ti_index<len(temp1):
                        time_list.append(ti_index)
                        ti_index=ti_index+1
            elif text.find(temp1[ti_index])<text.find(temp2[tr_index]):
               #     print('2')
                text=get_text(text,temp1[ti_index])
                if text.find(temp1[ti_index+1])>text.find(temp2[tr_index]):
                 #       print('2-1')
                    text=get_text(text,temp2[tr_index])
                    ti_index=ti_index+1
                    tr_index=tr_index+1
                    if tr_index==len(temp2):
                        while ti_index<len(temp1):
                            time_list.append(ti_index)
                            ti_index=ti_index+1
                else:
                   #     print('2-2')
                    time_list.append(ti_index)
                    ti_index=ti_index+1
        else:
            if (len(temp1)-len(time_list))<(len(temp2)-len(treat_list)):
                #print('3')
                if text.find(temp1[ti_index])<text.find(temp2[tr_index]):
                  #      print('3-1')
                    text=get_text(text,temp2[tr_index])
                    ti_index=ti_index+1
                    tr_index=tr_index+1
                    if ti_index==len(temp1):
                        while tr_index<len(temp2):
                            treat_list.append(tr_index)
                            tr_index=tr_index+1
                elif  text.find(temp1[ti_index])>text.find(temp2[tr_index]):
                    #    print('3-2')
                    text=get_text(text,temp2[tr_index])
                    if text.find(temp1[ti_index])<text.find(temp2[tr_index+1]):
                      #      print('3-3')
                        treat_list.append(tr_index)
                        text=get_text(text,temp2[tr_index+1])
                        tr_index=tr_index+2
                        ti_index=ti_index+1
                        if ti_index==len(temp1):
                            while tr_index<len(temp2):
                                treat_list.append(tr_index)
                                tr_index=tr_index+1
                    else:
                    #    print('3-4')
                        treat_list.append(tr_index)
                        treat_list.append(tr_index+1)
                        text=get_text(text,temp2[tr_index+1])
                        tr_index=tr_index+2
                        if tr_index==len(temp2):
                            while ti_index<len(temp1):
                                time_list.append(ti_index)
                                ti_index=ti_index+1
                
    time_temp=[]
    treat_temp=[]
    for i in range(0,len(temp1)):
        if i not in time_list:
            time_temp.append(new_time[i])
    for i in range(0,len(temp2)):
        if i not in treat_list:
            treat_temp.append(temp2[i])
    for i in range(0,len(time_temp)):
        temp.append(time_temp[i])
        temp.append(treat_temp[i])
    return temp


if __name__ == '__main__':
    text = """
判决如下：</div><a type='dir' name='PJJG'></a><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>一、被告人游红武犯受贿罪，判处有期徒刑五年三个月，并处没收财产人民币五万元（刑期从判决执行之日起计算，判决执行以前先行羁押的，羁押一日折抵刑期一日，扣除先行羁押的七日，即从2014年9月1日起至2019年11月23日止）。</div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>二、被告人游红武退出的违法所得人民币23万元，上缴国库（上述款项现由广州市天河区人民检察院代管）。</div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>如不服本判决，可在接到判决书的第二日起十日内，通过本院或者直接向广东省广州市中级人民法院提出上诉。书面上诉的，应提交上诉状正本一份，副本二份。
"""
    #print([get_info("一、被告人张某某，",r'被告人')[-1]])
    #print([get_info(text,r'\s*被告人.*?[，。]|上诉人（?原审被告人）?.*?[，|。]')])

    print(paragraphing(text))
