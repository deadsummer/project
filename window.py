#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
import fileinput
import urllib.request
import codecs

import url2 as url2
#parser

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
	if n>300:
		return links
	else:
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
		for x in catlinks:
			links=pars_cat_link(x,links,n)
	return links
	
def pars(start_links,textbox):
	w = codecs.open('wiki.txt','w', encoding='utf-8')
	n=0
	for x in start_links:
		start_page=x
		textbox.delete('1.0', END) 
		textbox.insert(1.0,"Making links")
		links=[]
		text=""
		links=pars_cat_link(start_page, links,0)
		textbox.delete('1.0', END) 
		textbox.insert(2.0,"Done "+str(len(links))+" total links\nDeleting similar")
		links=set(links)
		textbox.delete('1.0', END) 
		textbox.insert(3.0,"Done "+str(len(links))+" different links\nMaking text")
		print("Making text")

		
		for x in links:
			n=n+1
			text=pars_text(x,text)
			#textbox.delete('1.0', END) 
			#textbox.insert(1.0,str(n)+"links")
	w.write(text)
	w.close()
#parser end


def _open():
	op = askopenfilename()
	for l in fileinput.input(op):
		txt.insert(END,l)

root = Tk()
f=Frame(root,width=800,height = 400)
f.pack()
m = Menu(root)
root.config(menu=m)

fm = Menu(m)
m.add_cascade(label="File",menu=fm)
fm.add_command(label="Open...",command=_open)

def parsing():
	a=cat1.get()
	b=cat2.get()
	print(a)
	print(b)
	pars([a,b],t)
	
def analising():
	final=url2.analis()
	for x in final:
		for k in x:
			result.insert(1.0,k+"\t")
		result.insert(1.0,"\n")
			
			
lab1=Label(f,text='Категория 1',width=13,height=1,font='arial 10')
lab2=Label(f,text='Категория 2',width=13,height=1,font='arial 10')
lab1.place(x=20,y=10)
lab2.place(x=20,y=60)

cat1=Entry(width=50)
cat1.place(x=160,y=10)

cat2=Entry(width=50)
cat2.place(x=160,y=60)

pars_b=Button(f, text = 'Загрузить',command=parsing)
pars_b.place(x=200,y=100)


anal=Button(f, text = 'Анализировать',command=analising)
anal.place(x=400,y=100)


res_f=Frame(f,height=300,width=500)
res_f.place(x=30,y=140)
result=Text(res_f,height=7,width=60,font='Arial 10',wrap=WORD)
result.pack(side=LEFT, fill=Y)
scrollbar = Scrollbar(res_f)
scrollbar.pack(side=RIGHT, fill=Y)
# первая привязка
scrollbar['command'] = result.yview
# вторая привязка
result['yscrollcommand'] = scrollbar.set

t=Text(f,height=1,width=60,font='Arial 10',wrap=WORD)
t.place(x=30,y=340)

root.mainloop()

