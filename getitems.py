from urllib import urlopen
from StringIO import StringIO
import gzip
from bs4 import BeautifulSoup

url = 'http://boardgamegeek.com/boardgame/'
class BoardGameParser:

    def __init__(self, gameUrl):
        response = urlopen(gameUrl)
        if response.info().get('Content-Encoding') == 'gzip':       
            buffer = StringIO(response.read())
            html_doc = gzip.GzipFile(fileobj=buffer)
            #print html_doc.read(100)
            buffer.close
        else:
            html_doc = response.read()
            
        self.soup = BeautifulSoup(html_doc)



    def getNameOfGame(self):
        #response = urlopen(gameUrl)
        #if response.info().get('Content-Encoding') == 'gzip':

        #    buffer = StringIO(response.read())
        #    html_doc = gzip.GzipFile(fileobj=buffer)
        #    #print html_doc.read(100)
        #    buffer.close
        #else:
        #    html_doc = response.read()


        #soup = BeautifulSoup(html_doc)
        if self.soup.find('b') == None: 
            return ''
        elif self.soup.b.text == 'Error: Could not view GeekItem':
            return ''
        else:
            return self.soup.h1.span.text

    def getInfoByCategoryName(self, categoryName):
        if (self.soup.find('b') == None):
            return ''
        elif self.soup.b.text == 'Error: Could not view GeekItem':
            return ''
        elif self.soup.find('table', class_='geekitem_infotable').find('b',text=categoryName) == None:
            return ''
        else:

            newsoup= StringIO(self.soup.find('table', class_='geekitem_infotable').find('b',text=categoryName).find_next('td'))
            newsoup = BeautifulSoup(newsoup)
            
            if newsoup.find('a') == None:
                return newsoup.text.strip()
            else:
                result = ''
                for text in newsoup.find_all('a'):
                    result = result + text.text + ', '
                    
                return result

for i in xrange(355,1000):
    gurl=url+str(i)
    
    #print gurl
    print "id:", i
    game = BoardGameParser(gurl)
    print "\tName of Game:", game.getNameOfGame()
    print '\tCategory:', game.getInfoByCategoryName('Category')
    print '\tDesigner:', game.getInfoByCategoryName('Designer')
    print '\tYear Published:', game.getInfoByCategoryName('Year Published')
