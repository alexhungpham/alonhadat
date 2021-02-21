import os
import re
import json
import time
import pandas as pd
import string
from datetime import date
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
recorddate = str(date.today())
session = HTMLSession()
from pandas import DataFrame
exportPath = 'data/'

newsdict = {'http://tapchinganhang.com.vn/tin-tuc.htm','http://tapchinganhang.com.vn/co-che-chinh-sach.htm','http://tapchinganhang.com.vn/tai-chinh-quoc-te.htm','http://tapchinganhang.com.vn/giao-duc-tai-chinh.htm','http://tapchinganhang.com.vn/du-lieu-tcnh.htm','http://tapchinganhang.com.vn/gioi-thieu-toa-soan.htm','http://tapchinganhang.com.vn/tap-chi-ngan-hang.htm','http://tapchinganhang.com.vn/thu-vien-du-lieu.htm','http://tapchinganhang.com.vn/lien-he.htm','http://tapchinganhang.com.vn/cong-nghe-ngan-hang.htm','http://tapchinganhang.com.vn/hoat-dong-ngan-hang.htm','http://tapchinganhang.com.vn/nghien-cuu-trao-doi.htm','http://tapchinganhang.com.vn/thi-truong-tai-chinh.htm','https://www.vietcombank.com.vn/'}
news_links = []
news_hosts = [
            'http://tapchinganhang.com.vn/cong-nghe-ngan-hang.htm',
            'http://tapchinganhang.com.vn/cong-nghe-ngan-hang/trang-2.htm',
            'http://tapchinganhang.com.vn/cong-nghe-ngan-hang/trang-3.htm',
            'http://tapchinganhang.com.vn/cong-nghe-ngan-hang/trang-4.htm',
            'http://tapchinganhang.com.vn/cong-nghe-ngan-hang/trang-5.htm',
            'http://tapchinganhang.com.vn/cong-nghe-ngan-hang/trang-6.htm',
            'http://tapchinganhang.com.vn/cong-nghe-ngan-hang/trang-7.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-2.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-3.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-4.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-5.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-6.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-7.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-8.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-9.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-10.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-11.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-12.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-13.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-14.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-15.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-16.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-17.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-18.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-19.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-20.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-21.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-22.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-23.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-24.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-25.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-26.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-27.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-28.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-29.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-30.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-31.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-32.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-33.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-34.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-35.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-36.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-37.htm',
            'http://tapchinganhang.com.vn/hoat-dong-ngan-hang/trang-38.htm',
            'http://tapchinganhang.com.vn/nghien-cuu-trao-doi.htm',
            'http://tapchinganhang.com.vn/nghien-cuu-trao-doi/trang-2.htm',
            'http://tapchinganhang.com.vn/nghien-cuu-trao-doi/trang-3.htm',
            'http://tapchinganhang.com.vn/thi-truong-tai-chinh.htm',
            'http://tapchinganhang.com.vn/thi-truong-tai-chinh/trang-2.htm',
            'http://tapchinganhang.com.vn/thi-truong-tai-chinh/trang-3.htm',            
            ]
for i in range(len(news_hosts)):
    found_link = session.get(news_hosts[i]).html.absolute_links
    for link in found_link:
        if re.search("http://tapchinganhang.com.vn/&ni=69&p=",link):
            link = ""
        elif re.search("http://tapchinganhang.com.vn/tcnh-so-",link):
            link = ""
        elif re.search("http://tapchinganhang.com.vn/thu-vien-anh",link):
            link = ""
        elif link in newsdict:
            link = ""
        elif re.search("http://tapchinganhang.com.vn/",link):
            news_links.append(link)
        else:
            link = ""

            
            
news_c = []
news_t = []
for news in news_links:
    news_target = news
    r=session.get(news_target)
    c = r.html.xpath('//*[@id="new"]/div[1]/div[2]/div[2]/div[2]/*')
    r.html.xpath('//*[@id="new"]/div[1]/div[1]/div[2]/div[2]/div[1]/text()')
    news_title = r.html.xpath('//*[@id="new"]/div[1]/div[1]/div[1]/h1/text()')
    news_t.append(news_title)
        # newsitems['title'].append(news_title)
    content = []
    news_content= ''
    for x in range(len(c)):
        path = '//*[@id="new"]/div[1]/div[1]/div[2]/div[2]/div['+str(x+1)+']/text()'
        content.append(r.html.xpath(path))
    news_content =''.join(str(i) for i in content)
    news_c.append(news_content)

df = pd.DataFrame({'titles': news_t,'contents':news_c})
df.to_csv (r'data/'+recorddate+'.csv',encoding='utf-8')



