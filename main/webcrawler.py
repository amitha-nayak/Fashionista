from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup
import os,json

def webcrawler(m):

    print("here")
    label_description_path=r'../../label_descriptions.json'
    with open(label_description_path, 'r') as file:
        label_desc = json.load(file)
    print("finally here")
    links=[]
    #m=['symmetrical jacket','collarless collar','wrist-length sleeve']
    #print(m)
    w1="-".join(m).replace(' ','-')
    w2="+".join(m).replace(' ','+')
    w3="%20".join(m).replace(' ','%20')


    #Website1
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    s = HTMLSession()
    res = s.get("https://www.myntra.com/"+w1+"?p=1&plaEnabled=false", headers=headers, verify=False)

    soup = BeautifulSoup(res.text,"html.parser")
    #print(soup.html)

    val=json.loads(soup.find_all('script', type='application/ld+json')[1].string)
    linksw1=[]
    for i in val['itemListElement']:
        linksw1.append(i['url'])
    #print(linksw1)
    links.extend(linksw1[0:2])

    #Website2
    linksw2=[]
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    s = HTMLSession()
    res = s.get("https://www2.hm.com/en_in/search-results.html?q="+w2, headers=headers, verify=False)

    soup = BeautifulSoup(res.text,"lxml")
    #print(soup.html)
    if(soup.find_all('h1', attrs={'class': 'heading'})[0].contents[0]=='NO MATCHING ITEMS')==True:
        links.extend(linksw1[2:4])
    else:
        for item in soup.select('.hm-product-item'):
            linksw2.append(item.select('.item-link')[0]['href'])
        links.extend(linksw2[0:2])

    #website3
    linksw3=[]
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    s = HTMLSession()
    res = s.get("https://www.ajio.com/search/?text="+w3, headers=headers, verify=False)

    soup = BeautifulSoup(res.text,"html.parser")
    #print(soup.html)
    try:
      val=json.loads(soup.find_all('script', type='application/ld+json')[2].string)
    except:
      links.extend(linksw1[4:6])

    for i in val['itemListElement']:
        linksw3.append(i['url'])
    #print(linksw3)
    links.extend(linksw3[0:2])

    #print("final")
    return links
