import math

def split(base, url, i=0):
	basenum = charNum(base, "/")
	num = charNum(url, "/")
	num = (num - basenum) + 1
	spl = url.rsplit("/", num)	
	if(i == 1):
		spl = spl[:-1]
	
	return spl
	
def charNum(string, char):
	num = 0
	i = 0
	while(i != -1):
		i = string.find(char, i)
		if(i != -1):
			num += 1
			i += 1
	return num

def repl(link, replace, char, base):
	if(link[-1] == "/"):
		link = link[:-1]
	
	if(base[-1] == "/"):
		base = base[:-1]
	
	spl = link.rsplit("/")
	i = -1
	while(math.fabs(i) <= len(spl)):
		if(spl[i] == ".."):
			spl[i] = replace[i]
			
		if(replace[i] == base):
			spl = spl[i:]
			break
		i -= 1
	
	link = ""
	for i in spl:
		link += "/" + i
	return link
	
def process(url, link, base):
	if(link[:4] == "http" or link[:4] == "file" or link[:4] == "mail"):
		pass
	else:
		if(link[:2] == "./"):
			link = link[2:]
			spl = split(base, url, 1)
			url = ""
			for i in spl:
				url += i + "/"
			
			link = url + link
		elif(link[:2] == ".."):
			spl = split(base, url)
			link = repl(link, spl, "/", base)
			if(base[-1] == "/"):
				link = link[1:]
			link = base + link
		else:
			spl = split(base, url, 1)
			url = ""
			for i in spl:
				url += i + "/"
			
			link = url + link
	return link

def main():
	url = "http://localhost:41130"
	link = "test1.html"
	base = "http://localhost:41130"

	newlink = process(url, link, base)
	print newlink
	
if __name__ == '__main__':
	main()