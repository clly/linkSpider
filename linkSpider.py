import urllib, sys, os
import joinURL, Parser, Sitelib
	
	
class link:
	def __init__(self, url, cameFrom):
		self.code = 0
		self.url = url
		self.follow = False
		self.cameFrom = cameFrom
		
	
def top(url):
	num = joinURL.charNum(url, "/") - 2
	spl = url.rsplit("/", num)
	spl = spl[:-1]
	for i in spl:
		url = i + "/"
	return url
		
def spider(url, base):
	site = Sitelib.SiteLinks(link(url, "start"), base)
	numlinks = 1
	while(site.todo):
		l = site.todo[0]
		belong = site.belong(l.url)
		if(not site.checked(l.url) and belong):
			print "link " + str(numlinks) + ": " + l.url
			req = urllib.urlopen(l.url)

			l.code = req.getcode()
			l.follow = belong
			if(l.code == 200):
				if(l.follow):
					html = req.read()
					site.liveLinks.append(l)
					findLinks(html, l.url, site)
				else:
					site.liveLinks.append(l)
			else:
				site.deadLinks.append(l)

			site.searched.append(l.url)
			#print(site.searched)
			req.close()
			numlinks += 1
			
		site.todo.pop(0)
	
	print(site.printLive())
	print(site.printDead())
	print str(numlinks) + " links searched"
		
def findLinks(html, url, site):
	myparser = Parser.Parser()
	myparser.feed(html)
	hyperlinks = myparser.getHyperlinks()
	
	for i in range(len(hyperlinks)):
		hyperlinks[i] = link(joinURL.process(url, hyperlinks[i], site.base), url)
		
	for i in range(len(hyperlinks)):
		if(site.checked(hyperlinks[i])):
			pass
		else:
			site.todo.append(hyperlinks[i])
		
def main():
	if(len(sys.argv) > 1):
		url = sys.argv[1]
	else:
		url = "http://wgi/index.html"
	base = top(url)
	spider(url, base)
	
if __name__ == '__main__':
	main();