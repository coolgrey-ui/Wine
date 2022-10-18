from bs4 import BeautifulSoup
from selenium import webdriver
import cx_Oracle

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',options=options)


cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle64odac")
dsn = cx_Oracle.makedsn("10.35.2.11", 1521, service_name = "SKYSHOPBI") # 오라클 주소
connection = cx_Oracle.connect(user="gugudan", password="gugudan", dsn=dsn, encoding="UTF-8")
cur = connection.cursor() # 실행 결과 데이터를 담을 메모리 객체
sql_tot = "select count(*) from WN_PRDT_MASTER"
sql_se = "select WN_CODE from WN_PRDT_MASTER where WN_SEQ = :1"

rs_tot = cur.execute(sql_tot)
for record in rs_tot:
        print(record[0])
        total_cnt = record[0]

# total_cnt = 10
for i in range(total_cnt):
    seq = i+1
    t_se = (seq,)
    rs = cur.execute(sql_se,t_se)	#--execute => sql문 실행
    for record in rs:
        print(record[0])
        code = record[0]
    ######################################################################################
    # code = '170420'
    url = 'https://www.wine21.com/13_search/wine_view.html?Idx='+code 
    wd.get(url)
    soup_sel = BeautifulSoup(wd.page_source, 'html.parser')
    tastingnote = ''
    if soup_sel.find_all('div', attrs={'class': 'makers-item-txt'}):
        tastingnote = soup_sel.find_all('div', attrs={'class': 'makers-item-txt'})[0].getText()
        print('TASTINGNOTE       :', tastingnote)

    ######################################################################################

    sql_up = "update WN_PRDT_MASTER set WN_TASTINGNOTE = :1 where WN_SEQ = :2"
    # print(sql_up)
    t_up = (tastingnote,seq)
    # print(t_up)
    rs_up = cur.execute(sql_up,t_up)


cur.close()
connection.commit()
connection.close()