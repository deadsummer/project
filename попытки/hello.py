import re
import unittest

class Stemmer:
    # Helper regex strings.
    _vowel = "[аеиоуыэюя]"
    _non_vowel = "[^аеиоуыэюя]"
 
    # Word regions.
    _re_rv = re.compile(_vowel)
    _re_r1 = re.compile(_vowel + _non_vowel)
 
    # Endings.
    _re_perfective_gerund = re.compile(
        r"(((?P<ignore>[ая])(в|вши|вшись))|(ив|ивши|ившись|ыв|ывши|ывшись))$"
    )
    _re_adjective = re.compile(
        r"(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|"
        r"ую|юю|ая|яя|ою|ею)$"
    )
    _re_participle = re.compile(
        r"(((?P<ignore>[ая])(ем|нн|вш|ющ|щ))|(ивш|ывш|ующ))$"
    )
    _re_reflexive = re.compile(
        r"(ся|сь)$"
    )
    _re_verb = re.compile(
        r"(((?P<ignore>[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|"
        r"нно))|(ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|"
        r"ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю))$"
    )
    _re_noun = re.compile(
        r"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|"
        r"ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$"
    )
    _re_superlative = re.compile(
        r"(ейш|ейше)$"
    )
    _re_derivational = re.compile(
        r"(ост|ость)$"
    )
    _re_i = re.compile(
        r"и$"
    )
    _re_nn = re.compile(
        r"((?<=н)н)$"
    )
    _re_ = re.compile(
        r"ь$"
    )
 
    def stem(self, word):
        """
        Gets the stem.
        """
 
        rv_pos, r2_pos = self._find_rv(word), self._find_r2(word)
        word = self._step_1(word, rv_pos)
        word = self._step_2(word, rv_pos)
        word = self._step_3(word, r2_pos)
        word = self._step_4(word, rv_pos)
        return word
 
    def _find_rv(self, word):
        """
        Searches for the RV region.
        """
 
        rv_match = self._re_rv.search(word)
        if not rv_match:
            return len(word)
        return rv_match.end()
 
    def _find_r2(self, word):
        """
        Searches for the R2 region.
        """
 
        r1_match = self._re_r1.search(word)
        if not r1_match:
            return len(word)
        r2_match = self._re_r1.search(word, r1_match.end())
        if not r2_match:
            return len(word)
        return r2_match.end()
 
    def _cut(self, word, ending, pos):
        """
        Tries to cut the specified ending after the specified position.
        """
 
        match = ending.search(word, pos)
        if match:
            try:
                ignore = match.group("ignore") or ""
            except IndexError:
                # No ignored characters in pattern.
                return True, word[:match.start()]
            else:
                # Do not cut ignored part.
                return True, word[:match.start() + len(ignore)]
        else:
            return False, word
 
    def _step_1(self, word, rv_pos):
        match, word = self._cut(word, self._re_perfective_gerund, rv_pos)
        if match:
            return word
        _, word = self._cut(word, self._re_reflexive, rv_pos)
        match, word = self._cut(word, self._re_adjective, rv_pos)
        if match:
            _, word = self._cut(word, self._re_participle, rv_pos)
            return word
        match, word = self._cut(word, self._re_verb, rv_pos)
        if match:
            return word
        _, word = self._cut(word, self._re_noun, rv_pos)
        return word
 
    def _step_2(self, word, rv_pos):
        _, word = self._cut(word, self._re_i, rv_pos)
        return word
 
    def _step_3(self, word, r2_pos):
        _, word = self._cut(word, self._re_derivational, r2_pos)
        return word
 
    def _step_4(self, word, rv_pos):
        _, word = self._cut(word, self._re_superlative, rv_pos)
        match, word = self._cut(word, self._re_nn, rv_pos)
        if not match:
            _, word = self._cut(word, self._re_, rv_pos)
        return word

		
def max_similar(words, basis):
	n=len(basis)
	basis_words = list(map(st.stem,words))
	print(basis_words)

	similarity=[0]*n
	for i in range (n):
		for j in range (len(basis_words)):
			for q in range (len(basis[i])):
				if (basis_words[j]==basis[i][q]):
					similarity[i]+=1
					break
	a=max(similarity)
	print(a)
	#сделано в два прохода, сделать в один
	result=[]
	for i in range (n):
		if similarity[i]==a:
			result.append(i)
	return(result)
	
def one_similar(words, basis):
	n=len(basis)
	basis_words = list(map(st.stem,words))
	print(basis_words)

	similarity=[0]*n
	for i in range (n):
		for j in range (len(basis_words)):
			for q in range (len(basis[i])):
				if (basis_words[j]==basis[i][q]):
					similarity[i]+=1
					break
	a=max(similarity)
	print(a)
	#сделано в два прохода, сделать в один
	result=[]
	for i in range (n):
		if similarity[i]>0:
			result.append(i)
	return(result)

import codecs
f = codecs.open('data.txt', encoding='utf-8')

def split_text(f):
	data = f.readlines()
	j=0
	s=[]
	for par in data:
		k1=0
		start=0
		while par.find(".",start)!=-1:
			
			k2=par.find(".",start)
			if (par[k2+2].istitle() or par[k2+2].isspace()):
				#print(par[k2+2])
				s.append(par[k1:k2])
				k1=k2+2
				start=k2+2
			elif (par[k2+1].istitle()or par[k2+2].isspace()):
					s.append(par[k1:k2])
					k1=k2+1
					start=k2+1
			else:
					start=k2+1
	for i in range (len(s)):
		s[i]=s[i].lower()
	return s

def del_space(s):
	n=len(s)
	for i in range (n):
			while s[i][0:1]==" ":
				s[i]=s[i][1:]
			if len(s[i])==0: 
				del s[i]
			if s[i]=="\r\n":
				del s[i]
	return s

#def split_word(s):
#	n=len(s)
#	sent=["0"]*n
#	for i in range(n):
#		sent[i] = s[i].split()
#		for j in range (len(sent[i])):
#			if (sent[i][j][-1].islower()==False):
#				sent[i][j]=sent[i][j][:-2]
#	return(sent)
	
def split_sent(string):
	words = string.split()
	for j in range (len(words)):
		if (words[j][-1].islower()==False):
			words[j]=words[j][:-2]
	return(words)

def stem_without_prepos(word):
	a=st.stem(word)
	if len(a)>1:
		return a
	else:
		return "$%prep$%"

st=Stemmer()

s=split_text(f)
s=del_space(s)
sent=[]
for x in s:
	sent.append(split_sent(x))

basis=list(map(lambda x: list(map(stem_without_prepos,x)),sent))
print("Ready///")

#Задача первая: Найти предложение, максимально похожее на введенное
def word_sim():
	ask="0";
	while ask!="exit":
		ask=input()
		ask_w=ask.split()
		output=open("output.txt","wb")
		for j in max_similar(ask_w,basis):
			output.write(s[j].encode("utf-8"))
			output.write(b"\r\n")
			output.write(str(basis[j]).encode("utf-8"))
			output.write(b"\r\n")
		output.close()
	return(0)
	
#Задача вторая: разбиение предложений на логические участки, слова из разных не суммируются
# p = codecs.open('prepos.txt', encoding='utf-8')
# pr = p.readlines()
# prepos=pr[0]
# prep=prepos.split()
# sent2=[]
# s2=[]
# basis2=[]
# for j in one_similar(prep,basis):
# 	s2.append(s[j])
# 	sent2.append(sent[j])
# 	basis2.append(basis[j])
# output=open("output.txt","wb")
# for j in range (len(s2)):
# 	output.write(s2[j].encode("utf-8"))
# 	output.write(b"\r\n")
# output.close()

class Statement:
	string=""
	prich=[]
	sled=[]
	def __init__(self,string):
		self.string=string
	

prep_list=["чт", "где", "когда", "потому", "если", "то", "котор"]
	
statements=[]
for i in range (len(s)):
	for j in range (len(prep_list)):
		x=s[i].find(prep_list[j])
		if x!=-1:
			break
	if x==-1:
		continue
	p=Statement(s[i])
	y=p.string.rfind(",",0,x)
	z=p.string.find(" ",x)
	p.prich=split_sent(p.string[0:y])
	p.sled=split_sent(p.string[z:])
	statements.append(p)

output=open("output.txt","wb")
for j in statements:
	output.write(j.string.encode("utf-8"))
	output.write(b"//")
	output.write(str(j.prich).encode("utf-8"))
	output.write(b"//")
	output.write(str(j.sled).encode("utf-8"))
	output.write(b"\r\n")
output.close()


input()