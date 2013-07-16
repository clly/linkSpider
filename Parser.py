from HTMLParser import HTMLParser

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.a = 0
        self.hyperlinks = []
    
    def handle_starttag(self, tag, attrs):
        if(tag == 'a'):
            if(attrs[0][0] == "href"):
                self.hyperlinks.append(attrs[0][1])
                self.a = True
            
    def handle_endtag(self, tag):
        if(tag == 'a'):
            self.a = False
    
    def getHyperlinks(self):
        return self.hyperlinks
        
