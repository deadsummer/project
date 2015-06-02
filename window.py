#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
import fileinput
import urllib.request
import codecs
from bs4 import BeautifulSoup
import analis as url2

import parser_sasha as par


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
	par.pars([a,b],t)
	
def analising():
	f1_f2=url2.analis()
	print(f1_f2)
	for u in f1_f2:
		for x in u:
			if len(x)==0:
				for k in x:
					result.insert(1.0,k+"\t")
			result.insert(1.0,"\n")
		result.insert(1.0,"\n------------\n")
			
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

