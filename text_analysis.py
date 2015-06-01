import re
import unittest
import urllib.request
import codecs

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

def split_text(string):
	string=string.replace("\n",".")
	s=[]
	k1=0
	start=0
	while string.find(".",start)!=-1:
		
		k2=string.find(".",start)
		if (len(string)>k2+3):
			if string[k2+2].istitle() or string[k2+2].isspace():
				#print(string[k2+2])
				s.append(string[k1:k2])
				k1=k2+2
				start=k2+2
			elif (string[k2+1].istitle()or string[k2+2].isspace()):
					s.append(string[k1:k2])
					k1=k2+1
					start=k2+1
			else:
					start=k2+1
		else:
					start=k2+1
		
	for i in range (len(s)):
		s[i]=s[i].lower()
	return s

def del_space(s):
	n=len(s)
	for i in range (n):
			while s[i][0:1]==".":
				s[i]=s[i][1:]
			while s[i][-1]==".":
				s[i]=s[i][:-2]
			while s[i][0:1]==".":
				s[i]=s[i][1:]
			if len(s[i])==0: 
				del s[i]
	return s
	
def split_sent_simple(string):
	words=string.split()
	for j in range(len(words)):
		l=0
		while l<len(words[j]):
			if words[j][l].isalnum()==False:
				words[j]=words[j][:l]+words[j][l+1:]
			else:
				l=l+1

	j=0
	while j < len(words):
		if len(words[j])<1 or words[j].isdigit() or (words[j] in ("и","a","но","за","под","на","в","у","к","до","над","от","над","до","из","для","c","со","о")):
			del words[j]
		else:
			j=j+1
	return(words)

	
def stem(word):
	st=Stemmer()
	return(st.stem(word))
	
	