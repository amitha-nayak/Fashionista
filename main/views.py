import sys
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import ImageForm
import warnings
from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup
import os,json
warnings.filterwarnings("ignore")
sys.path.append('/home/jigyas15/t4/fash/kaggle-imaterialist2020-model')
from prediction import pre
# Create your views here.

def index(request):
    return render(None,'ind.html')

def test(request):
    if request.method=="POST":
        form=ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img_obj=form.instance
            print(request.POST)
            print(img_obj.image.url)
            return render(request,'test.html',{'form':form,'img_obj':img_obj,'alert':"success"})
    else:
        form=ImageForm()
    return render(request,'test.html',{'form':form})

def predict(request):
    if request.method=="POST":
        #print(request.POST['url'])
        if('imgg' in request.POST):
         print(request.POST['imgg'])
         val=pre(request.POST['imgg'])
        else:
         val=pre()
        print(val)
        os.system('sudo rm -r /tmp/images/')
        os.system('sudo rm -r /home/jigyas15/t4/fash/media/images')
        return render(request,"pred.html",val)


def pyfun(request):
    print("Hello")
    return render(request,"pred.html",{'major':['symmetrical skirt',
 'regular (fit) bag, wallet',
 'symmetrical jacket',
 'zip-up bag, wallet'],'minor':['collarless collar',
 'collarless neckline',
 'v-neck neckline',
 'wrist-length sleeve']})

def pred(request):
    if request.method=="POST":
        print("Im here")
        #os.system('sudo rm -r /home/jigyas15/t4/fash/media/images')
        m=[]
        m.append(request.POST['options1'])
        m.extend(request.POST.getlist('options2'))
        print(m)
        ans=webcrawler(m)
        return render(request,"tags.html",{'links':ans})
    return render(None,'pred.html')

def tags(request):
    if request.method=="POST":
        print(request.POST['options1'])
    return render(None,'tags.html')


def v1(request):
    return HttpResponse("<h1>Hello</h1>")

from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup
import os,json

def webcrawler(m):
    label_description_path=r'/home/jigyas15/dataset-iMaterialist/raw/label_descriptions.json'
    with open(label_description_path, 'r') as file:
        label_desc = json.load(file)

    links=[]
    #m=['symmetrical jacket','collarless collar','wrist-length sleeve']
    #print(m)
    w1="-".join(m).replace(' ','-')
    w2="+".join(m).replace(' ','+')
    w3="%20".join(m).replace(' ','%20')


    #Website1
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    s = HTMLSession()
    res = s.get("https://www.limeroad.com/search/"+w3, headers=headers)

    soup = BeautifulSoup(res.text,"html.parser")
    #print(soup.html)

    #val=json.loads(soup.find_all('script', type='application/ld+json')[1].string)
    v1=soup.find_all('a', attrs={'class': 'tdN c0'})
    linksw1=[]
    for i in v1:
        p2 = (i['href'].find("https",(i['href'].find("https"))+1))
        linksw1.append(i['href'][p2:])
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
      return links

    for i in val['itemListElement']:
        linksw3.append(i['url'])
    #print(linksw3)
    links.extend(linksw3[0:2])

    #print("final")
    return links
