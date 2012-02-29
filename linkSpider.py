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
		l.follow = site.belong(l.url)
		if(not site.checked(l) and l.follow):
			if("-v" in sys.argv):
				print "link " + str(numlinks) + ": " + l.url
			req = urllib.urlopen(l.url)
			l.code = req.getcode()
			if(l.code == 200):
				if(l.follow):
					html = req.read()
					site.liveLinks.append(l)
					findLinks(html, l.url, site)
				else:
					site.liveLinks.append(l)
			else:
				site.deadLinks.append(l)

			site.searched.append(l)
			#print(site.searched)
			req.close()
			numlinks += 1
			
		site.todo.pop(0)
	
	if("-l" in sys.argv or "-v" in sys.argv):
		site.printLive()
	site.printDead()
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
	if("-h" in sys.argv):
		print("\n    Usage: python linkSpider.py <args> <top url>\n" \
			"\t-h: this help message\n" \
			"\t-v: verbose output\n" \
			"\t-l: print live links as well as dead links\n" \
			"\t-o: check for live or dead links outside the domain")
		sys.exit(0)
	if(len(sys.argv) > 1):
		url = sys.argv[-1]
	else:
		print("\n    Usage: python linkSpider.py <args> <top url>\n" \
			"\t-h: this help message\n" \
			"\t-v: verbose output\n" \
			"\t-l: print live links as well as dead links\n" \
			"\t-o: check for live or dead links outside the domain")
		sys.exit(0)
	base = top(url)
	spider(url, base)
	
	print("Press enter to continue")
	
	
if __name__ == '__main__':
	main();