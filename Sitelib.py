import sys

class SiteLinks:
    def __init__(self, url, base):
        self.todo = [url]
        self.deadLinks = []
        self.liveLinks = []
        self.searched = []
        self.base = base
        
    def checked(self, link):
        """checks if the page has already been read"""
        check = False
        for i in self.searched:
            if(i.url == link.url and i.cameFrom == link.cameFrom):
                check = True
                break
            else:
                check = False
        return check
    
    def inArray(self, ext, urlExt):
        """checks if the extension is in the accepted url extensions"""
        for i in ext:
            if(i == urlExt):
                htmlPage = True
                break
            else:
                htmlPage = False
        
        return htmlPage
    
    def belong(self, url):
        """Checks whether or not the link will end up as an html page.
        To avoid reading in pdf's, downloadable files, etc"""
        check = False
        ext = ["html", "htm", "asp", "php", "shtml", "pl", "cgi", "", "md"]
        urlExt = url.rsplit(".", 1)[-1]
        if("-o" in sys.argv):
            if(self.inArray(ext, urlExt) or url == self.base):
                check = True
        elif(url[:len(self.base)]==self.base and self.inArray(ext, urlExt)):
            check = True
        elif(url == self.base):
            check = True
        else:
            check = False
        
        return check
    
    def printToDo(self):
        print("To Do:")
        for i in self.todo:
            print(i)
        print("\n")

    def printLive(self):
        print("Live Links:")
        for i in self.liveLinks:
            print(i.cameFrom + "   ->   " + i.url)
        print("\n")
    
    def printDead(self):
        print("Dead Links:")
        for i in self.deadLinks:
            print(i.cameFrom + "   ->   " + i.url)
        print("\n")
