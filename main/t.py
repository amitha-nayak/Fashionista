from requests_html import HTMLSession
import requests	
import json
from bs4 import BeautifulSoup
import os,json
from webcrawler import webcrawler
import warnings
warnings.filterwarnings("ignore")
m=['symmetrical jacket','collarless collar','wrist-length sleeve']
w1="-".join(m).replace(' ','-')
w2="+".join(m).replace(' ','+')
w3="%20".join(m).replace(' ','%20')
links=[]
#headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
print('before')
s = HTMLSession()
#s = requests.Session()
proxies = {'http': 'http://163.44.152.22:8080'} 
print("atfer 1")
print("https://www.myntra.com/"+w1+"?p=1&plaEnabled=false")
res = s.get("https://www.limeroad.com/search/"+w3, headers=headers)
print("after 2")
soup = BeautifulSoup(res.text,"html.parser")
#print(soup.html)

val=json.loads(soup.find_all('script', type='application/ld+json')[1].string)
linksw1=[]
for i in val['itemListElement']:
    linksw1.append(i['url'])
#print(linksw1)
links.extend(linksw1[0:2])
#ans=webcrawler(m)
print(links)
