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
               "User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36",
                }

        params = {'q':item,"page" : i,
        }
        res = requests.get("https://www.coupang.com/np/search?component=&channel=user",headers=headers,params=params)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.findAll('li',{'class':'plp-default__item'})
      
        b = soup.findAll('strong',{'class':'title'})
        for i in range(len(a)):
             pCodeList.append([b[i].get_text(),a[i]['data-product-id']])
    #print(pCodeList)

    return pCodeList


def danawaCraw(pcode, page,name):
    reviewlist = []
    for idx in range(1,page+1) :
        headers = {"User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36"}
        params = {"productId" : pcode, "page":idx, "size":100, 'sortBy':'ORDER_SCORE_ASC','ratingSummary':True} #한번에 후기 100개씩 가져오기
        res = requests.get("https://www.coupang.com/vp/product/reviews?", headers = headers, params = params)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.findAll('div',{'class':'sdp-review__article__list__review__content js_reviewArticleContent'})
#
        for i in range(len(a)):
            reviewlist.append({'name':name,'review':a[i].get_text()})
    #print(reviewlist)
    return reviewlist

#걸리는 시간 측정
#start_time = time.time() 

wb =  Workbook()
ws1 = wb.active
ws1.title = 'result'
ws1.append(['제품명','리뷰'])
TotalReview = []

root = Tk()
lbl = Label(root, text="찾고자 하는 키워드를 검색해주세요")
lbl.pack()
 
txt = Entry(root)
txt.pack()
def button_pressed() :
    for p in getPcode(10,txt.get()): # 10 페이지 클로링, 1페이지당 20개 제품
        single = danawaCraw(p[1],2,p[0]) #후기 2페이지 가져오기 -> 총 200개
        for j in single:
            ws1.append([str(j['name']),j['review']])
    wb.save("./쿠팡 리뷰 수집 (쿠팡 랭킹 상위 200개 제품으로부터 최대 200개씩).xlsx")

 
btn = Button(root, text="OK" , command = button_pressed)
btn.pack()
root.mainloop()

#최종으로 걸리는 시간 파악
# print("--- %s seconds ---" %(time.time() - start_time))