import http.client
import mimetypes
from codecs import encode

import json
from pyexpat import native_encoding
from bs4 import BeautifulSoup
import requests 

import re

import math

import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle64odac")
dsn = cx_Oracle.makedsn("10.35.2.11", 1521, service_name = "SKYSHOPBI") # 오라클 주소
connection = cx_Oracle.connect(user="gugudan", password="gugudan", dsn=dsn, encoding="UTF-8")
cur = connection.cursor() # 실행 결과 데이터를 담을 메모리 객체
# WN_FOOD, WN_AROMA 추가
sql = "insert into WN_PRDT_MASTER values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25)"

# pre_cnt = 25214
# pre_cnt = 252
pre_cnt = 25953

# page = '1'
page_size = '50'
total_page = math.ceil(pre_cnt / int(page_size))
seq = 0

for i in range(1,total_page+1):
    page = str(i)
    #######################################################################
    conn = http.client.HTTPSConnection("www.wine21.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=filter;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("{\"KEY_WORD\":\"\",\"NO_PRICE\":true}"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=option;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    # page_size_str = "{\"page\":1,\"pageSize\":10}"
    # page_size_str = "{\"page\":1,\"pageSize\":"+'10'+"}"
    page_size_str = "{\"page\":"+page+",\"pageSize\":"+page_size+"}"

    # dataList.append(encode("{\"page\":1,\"pageSize\":10}"))
    dataList.append(encode("{\"page\":"+page+",\"pageSize\":"+page_size+"}"))

    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://www.wine21.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.wine21.com/13_search/wine_list.html',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '__utmz=41375524.1637722230.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=7287l34p45o1p3qf8ojdjnuh4q; __utmc=41375524; __utma=41375524.2039133520.1637722230.1642384646.1642392503.11; WINE_HISTORY=JTVCJTdCJTIyV0lORV9JRFglMjIlM0ExNzA0MTElMkMlMjJJTUFHRV9VUkwlMjIlM0ElMjJodHRwcyUzQSUyRiUyRndpbmUyMS5zcGVlZGdhYmlhLmNvbSUyRldJTkVfTVNUJTJGVElUTEUlMkYwMTcwMDAwJTJGVzAxNzA0MTEucG5nJTIyJTdEJTJDJTdCJTIyV0lORV9JRFglMjIlM0ExNzA0MTMlMkMlMjJJTUFHRV9VUkwlMjIlM0ElMjJodHRwcyUzQSUyRiUyRndpbmUyMS5zcGVlZGdhYmlhLmNvbSUyRldJTkVfTVNUJTJGSU1BR0UlMkYwMTcwMDAwJTJGVDAxNzA0MTNfMDAxLnBuZyUyMiU3RCUyQyU3QiUyMldJTkVfSURYJTIyJTNBMTcwNDEyJTJDJTIySU1BR0VfVVJMJTIyJTNBJTIyaHR0cHMlM0ElMkYlMkZ3aW5lMjEuc3BlZWRnYWJpYS5jb20lMkZXSU5FX01TVCUyRlRJVExFJTJGMDE3MDAwMCUyRlcwMTcwNDEyLnBuZyUyMiU3RCU1RA%3D%3D; __utmt=1; __utmb=41375524.7.10.1642392503; LQ_WL=JTdCJTIyZmlsdGVyJTIyJTNBJTIyJTdCJTVDJTIyS0VZX1dPUkQlNUMlMjIlM0ElNUMlMjIlNUMlMjIlMkMlNUMlMjJOT19QUklDRSU1QyUyMiUzQXRydWUlN0QlMjIlMkMlMjJvcHRpb24lMjIlM0ElMjIlN0IlNUMlMjJwYWdlJTVDJTIyJTNBMSUyQyU1QyUyMnBhZ2VTaXplJTVDJTIyJTNBMTAlN0QlMjIlMkMlMjJleHRyYUN0cmwlMjIlM0ElMjIlN0IlN0QlMjIlMkMlMjJnb0xpc3QlMjIlM0FmYWxzZSU3RA%3D%3D',
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/13_search/proc/ajax_wine_list.php", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))

    jsonObject2 = json.loads(data.decode("utf-8"))
    body = jsonObject2.get("html")
    cnt = jsonObject2.get("TotalCnt")

    # total_page = math.ceil(cnt / int(page_size))
    # total_page = math.ceil(pre_cnt / int(page_size))

    soup = BeautifulSoup(body, 'html5lib')
    soup.select('.thumb')

    # seq = 0
    for thumb in soup.select('.thumb'):
        # print('code       :', thumb.a['href'].split('(')[1].split(')')[0])
        # print('kor_nm       :', thumb.find_next(class_='btnView').text.split('   ')[0].strip())
        # print('eng_nm       :', thumb.find_next(class_='wine-name-en').text.strip())
        # print('category       :', thumb.find_next(class_='board-badge').text)
        # print('price       :', thumb.find_next(class_='price').text.split('(')[0].split('원')[0])
        # print('nation       :', thumb.find_next(class_='country').text)
        # print('region       :', thumb.find_next(class_='nation').text)
        # print('capacity       :', thumb.find_next(class_='price').text.split('(')[1].split('ml')[0])
        # print('winery       :', thumb.find_next(class_='winery').text)    
        # print('image       :', thumb.a.img['src'])    

        code = thumb.a['href'].split('(')[1].split(')')[0]
        kor_nm = thumb.find_next(class_='btnView').text.split('   ')[0].strip()
        eng_nm = thumb.find_next(class_='wine-name-en').text.strip()
        category = thumb.find_next(class_='board-badge').text
        # price = thumb.find_next(class_='price').text.split('(')[0].split('원')[0].strip().replace(',', '')
        # price = 0
        # if price == '가격정보없음':
        #     price = 0
        # price_num = int(price)
        nation = thumb.find_next(class_='country').text
        if thumb.find_next(class_='nation'):
            region = thumb.find_next(class_='nation').text
        # capacity = thumb.find_next(class_='price').text.split('(')[1].split('ml')[0]
        capacity = ''
        winery = thumb.find_next(class_='winery').text.replace(u'\xa0', u' ')
        image = thumb.a.img['src']

        seq += 1
        year = '0000'
        sweetness = 0
        acid = 0
        bodied = 0
        tannin = 0
        nation_region = ''
        variety = ''
        sty = ''
        alcohol = ''
        temperature = ''
        importer = ''
        tastingnote = ''

        food = ''
        aroma = ''
        
        ###################################
        # code = '170420'
        # code = '171616'
        url = 'https://www.wine21.com/13_search/wine_view.html?Idx='+code 
        print(url)
        print('-' * 80)
        res = requests.get(url) 

        soup_detail = BeautifulSoup(res.text, 'html5lib')
        if len(soup_detail.find_all('p')) > 2:
            year = soup_detail.find_all('p')[3].getText().split('(')[1].split(',')[0]
        print('year       :', year) 
        if len(soup_detail.find_all(class_='filter-grade')) > 0:            
            sweetness = len(soup_detail.find_all(class_='filter-grade')[0].find_all(class_='on'))
            acid = len(soup_detail.find_all(class_='filter-grade')[1].find_all(class_='on'))
            bodied = len(soup_detail.find_all(class_='filter-grade')[2].find_all(class_='on'))
            tannin = len(soup_detail.find_all(class_='filter-grade')[3].find_all(class_='on'))

        print('SWEETNESS       :', sweetness)        
        print('ACID       :', acid)        
        print('BODIED       :', bodied)        
        print('TANNIN       :', tannin)


        print('aromalist start')
        aroma_all = soup_detail.select('em[class*="aroma-"]')
        # print(repr(aroma_all))    
        if aroma_all:
            aroma_str = ''
            for aromalist in aroma_all:
                aroma_str = aroma_str + aromalist.find_next_siblings('p')[0].getText() + '|'
                print (aroma_str)
                print('aroma       :', aroma_str)
            aroma = aroma_str[0:-1]
        print('aromalist end')
        
        # exit()

        print('foodlist start')
        food_all = soup_detail.select('em[class*="food-"]')
        if food_all:
            food_str = ''
            for foodlist in food_all:
                food_str = food_str + foodlist.find_next_siblings('p')[0].getText() + '|'
                print (food_str)
                print('food       :', food_str)
            food = food_str[0:-1]
        print('foodlist end')


        # price,capacity 구하기(웹페이지 변경사항 반영) 
        if soup_detail.find_all(class_='wine-price'):
            wine_price = soup_detail.find_all(class_='wine-price')[0].find("strong").getText()
        print('wine_price       :', wine_price)
        # exit()
        price = 0
        if wine_price == '가격정보없음':
            wine_price = '0'
        wine_price = wine_price.replace(',',"")
        price = re.findall('[0-9]+', wine_price)
        print('price       :', price)
        price_num = int(price[0])

        if soup_detail.find_all(class_='wine-price'):
            wine_capacity = soup_detail.find_all(class_='wine-price')[0].find("strong").next_sibling
            wine_capacity = wine_capacity.split(',')[1]
            wine_capacity = re.findall('[0-9]+', wine_capacity)
            print('wine_capacity       :', wine_capacity)
            capacity_num = int(wine_capacity[0])
        # exit()
        
        tastingnote = soup_detail.find_all('div', attrs={'class': 'div.makers-item-txt'})
        print('TASTINGNOTE       :', tastingnote)
        tastingnote = ''
        print('-' * 80)

        if soup_detail.find(class_= "wine-d-box-info-list"):
            # count of dl
            dl = soup_detail.find(class_= "wine-d-box-info-list").select('dl')
            dl_cnt = len(soup_detail.find(class_= "wine-d-box-info-list").select('dl'))
            # print(dl_cnt) 
            for dl_e in dl:
                dt_v = dl_e.dt.getText().strip()
                dd_v = dl_e.dd.getText().strip().replace('\n', ' ').replace('\r', '')

                if dt_v == "국가/생산지역":
                    nation_region = dd_v
                elif dt_v == "주요품종":
                    variety = dd_v
                elif dt_v == "스타일":
                    sty = dd_v
                elif dt_v == "알코올":
                    alcohol = dd_v
                elif dt_v == "음용온도":
                    temperature = dd_v
                elif dt_v == "수입사":
                    importer = dd_v

                print(dt_v)
                print(dd_v)

                print('-' * 80)
    
            print('-' * 80)

        ###################################
    
        t = (seq,code,kor_nm,eng_nm,category,price_num,nation,region,capacity_num,year,sweetness,acid,bodied,tannin,winery,nation_region,variety,sty,alcohol,temperature,importer,tastingnote,image,food,aroma)
        print(t)
        print('-' * 80) 
        cur.execute(sql,t)	#--execute => sql문 실행
        print('rowcount       :', cur.rowcount)
        print('-' * 80)

        print('code       :', code)
        print('kor_nm       :', kor_nm)
        print('eng_nm       :', eng_nm)
        print('category       :', category)
        print('price       :', price)
        print('nation       :', nation)
        print('region       :', region)
        print('capacity       :', capacity)
        print('winery       :', winery)    
        print('image       :', image)

        print('-' * 80)
    #######################################################################


cur.close()
connection.commit()
connection.close()
