import urllib, argparse
import joinURL, Parser, Sitelib

parser = argparse.ArgumentParser(description="Link spider to find dead links")

parser.add_argument("top_url",
                    action="store",
                    help="Highest point to check under for dead links",
                    )

parser.add_argument("-v", "--verbose",
                    dest="verbose",
                    action="store_true",
                    help="verbose messages",
                    )

parser.add_argument("-l", "--live",
                    dest="live",
                    action="store_true",
                    help="print live and dead links",
                    )

verbose = 0
live = 0

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
            if(verbose):
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
    
    if(live or verbose):
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

    return hyperlinks
        
def main():
    base = top(args.top_url)
    spider(args.top_url, base)
    
    print("Press enter to continue")
    
    
if __name__ == '__main__':
    args = parser.parse_args()
    verbose = args.verbose
    live = args.live
    main()
