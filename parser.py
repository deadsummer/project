#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import codecs



from bs4 import BeautifulSoup
import re
w = codecs.open('wiki.txt','w', encoding='utf-8')

def GetURL(url):
    s = 'error'
    try:
        f = urllib.request.urlopen(url)
        s = f.read()
    except urllib.error.HTTPError:
        s = 'connect error'
    except urllib.error.URLError:
        s = 'url error'
    return s
 

def pars_text (link, text):
	s = BeautifulSoup(GetURL(link))
	nodispclass=["gallerytext","magnify","reference","mw-editsection","display:none","infobox vcard"]
	nodispid=["toc","bitch"]
	content=s.find(id="mw-content-text")
	hren=content.findAll(class_=nodispclass)
	for x in hren:
		x.extract()
	text=text+"\n"+content.get_text()
	return text
	
def pars_cat_link (link0,links,n):
	soup = BeautifulSoup(GetURL(link0))
	CatItems=soup.findAll(class_="CategoryTreeItem")
	
	catlinks=[]
	for x in CatItems:
		catlinks.append("http://ru.wikipedia.org"+x.find('a')['href'])
	Items=soup.find(class_="mw-category")
	links_text=[]
	if Items!=None:
		a=Items.findAll('a')
		for x in a:
			n=n+1
			links.append("http://ru.wikipedia.org"+x['href'])
			links_text.append(x.get_text())
			print(n)
	for x in catlinks:
		links=pars_cat_link(x,links,n)
	return links
	
start_page='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%B5%D0%BE%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D1%8F_%D1%82%D1%80%D0%B5%D1%83%D0%B3%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D0%BA%D0%B0'
print("Making links")
links=[]
text=""
links=pars_cat_link(start_page, links,0)
print("Done "+str(len(links))+" total links\nDeleting similar")
links=set(links)
print("Done "+str(len(links))+" different links\nMaking text")

n=0
for x in links:
	n=n+1
	text=pars_text(x,text)
	print(n)
w.write(text)
w.close()
print("Done")
