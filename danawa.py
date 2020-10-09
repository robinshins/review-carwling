#필요한 패키지 로딩
import time
import requests
from bs4 import BeautifulSoup
import json
import openpyxl
from openpyxl import Workbook
from tkinter import *



def getPcode(page,item):
    pCodeList = []
    for i in range(1,page+1):
        #print(i,"페이지 입니다")
        headers = {
               "Referer" : "http://search.danawa.com/mobile/dsearch.php?keyword=%EA%B0%95%EC%95%84%EC%A7%80%EC%82%AC%EB%A3%8C",
               "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
                }

        params = {"page" : i,'bMain':1, 'keyword':item,'originalQuery':item,'previousKeyword':item,'keywordType':1,'isApp':False,
        'list': 'list','volumeType':'allvs','addDelivery':'N'
        }

        res = requests.post("http://search.danawa.com/mobile/ajax/product/getProductList.ajax.php", headers = headers, data=params)
        #print(res.text)
        soup = BeautifulSoup(res.text, "html.parser")
        #print(soup)
        a = soup.findAll('a',{'class':'a_l1_t2 link_prod'})
        b = soup.findAll('p',{'class':'goods_title_10'})
        for i in range(len(a)):
            pCodeList.append([b[i],a[i]['href'][46:53]])

    return pCodeList


def danawaCraw(pcode, page,name):
    reviewlist = []
    headers = {'Host':'m.danawa.com',"Referer" : "http://m.danawa.com/product/product.html?", "User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36"}
    params = {"productCode" : pcode, "limit":20000, "offset":0, 'align':'Usefulness'}
    res = requests.get("http://m.danawa.com/product/mallProductOpinionListData.json?", headers = headers, params = params)
    #print(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    #print(soup)
    d = json.loads(res.text)
    for i in d['result']['data']['productOpinionList']:
        reviewlist.append({'name':name,'shopname':i['shopName'],'date':i['createDate'],'score':i['score'],'content':i['content']})
    #print(reviewlist)
    return reviewlist

#걸리는 시간 측정
#start_time = time.time() 

TotalReview = []

wb =  Workbook()
ws1 = wb.active
ws1.title = 'result'
ws1.append(['제품명','구매처','닐짜','점수','리뷰'])
root = Tk()
lbl = Label(root, text="찾고자 하는 키워드를 검색해주세요")
lbl.pack()
 
txt = Entry(root)
txt.pack()
def button_pressed() :
    try:
        for p in getPcode(50,txt.get()): # 상품군 1페이지
            single = danawaCraw(p[1],2,p[0]) # 5페이지 리뷰
            for j in single:
                ws1.append([str(j['name']),j['shopname'],j['date'],j['score'],j['content']])
    except ValueError: 
        print("dsad")

    wb.save("./리뷰 분석 결과.xlsx")


 

 
btn = Button(root, text="OK" , command = button_pressed)
btn.pack()
root.mainloop()
 
#최종으로 걸리는 시간 파악
# print("--- %s seconds ---" %(time.time() - start_time))