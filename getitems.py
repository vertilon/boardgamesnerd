#!/usr/bin/env python
from urllib import urlopen
from StringIO import StringIO
import gzip
from bs4 import BeautifulSoup
import sys
import codecs

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

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
           
        #html_doc = str(html_doc)
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
            return self.soup.h1.span.text #.decode(formatter='html')

    def getInfoByCategoryName(self, categoryName):
        if (self.soup.find('b') == None):
            return ''
        elif self.soup.b.text == 'Error: Could not view GeekItem':
            return ''
        elif self.soup.find('table', class_='geekitem_infotable').find('b',text=categoryName) == None:
            return ''
        else:

            newsoup= self.soup.find('table', class_='geekitem_infotable').find('b',text=categoryName).find_next('td').prettify()
            newsoup = BeautifulSoup(newsoup)
            
            if newsoup.find('a') == None:
                return newsoup.text.strip().replace('\n','').replace('\t','')
            else:
                result = ''
                for text in newsoup.find_all('a'):
                    result = result + text.text.strip().replace('\n','').replace('\t','')+ ', '
                    
                return result
    def getDescription(self):
        if (self.soup.find('b') == None):
            return ''
        elif self.soup.b.text == 'Error: Could not view GeekItem':
            return ''
        elif self.soup.find('div', class_='wiki') == None:
            return ''
        else:
            return '\n'.join(str(self.soup.find('div', class_='wiki')).split('\n')[1:-1]).replace('\n','\\n')
xmlFile = codecs.open('boardgamegeek.xml','w','utf-8')
xmlFile= codecs.open('boardgamegeek.xml','r+','utf-8')
if xmlFile.readline() == '<add>':
    xmlFile = codecs.open ('boardgamegeek.xml','a','utf-8')
xmlFile.write('<add>\n')

def writeFieldToXml(xmlFile, name, value):
    string = ' <field name=\"'+name+'\">' + str(value) + '</field>\n'
    xmlFile.write(string)

for i in xrange(1,10000):

    gurl=url+str(i)


    xmlFile.write('<doc>\n')
    #print gurl
    writeFieldToXml(xmlFile, "id", i)
    game = BoardGameParser(gurl)
    
    #print "\tName of Game:", game.getNameOfGame()
    writeFieldToXml(xmlFile, "Name", game.getNameOfGame())

    #print '\tCategory:', game.getInfoByCategoryName('Category')
    writeFieldToXml(xmlFile, "Category", game.getInfoByCategoryName('Category'))

    #print '\tDesigner:', game.getInfoByCategoryName('Designer')
    writeFieldToXml(xmlFile, "Designer", game.getInfoByCategoryName('Designer'))

    #print '\tYear Published:', game.getInfoByCategoryName('Year Published')
    writeFieldToXml(xmlFile, "Year Published", game.getInfoByCategoryName('Year Published'))
    writeFieldToXml(xmlFile, "Numder of Players", game.getInfoByCategoryName('# of Players'.encode('utf-8')))
    writeFieldToXml(xmlFile, "Playing Time", game.getInfoByCategoryName('Playing Time'))
    writeFieldToXml(xmlFile, "Mfg Suggested Ages", game.getInfoByCategoryName('Mfg Suggested Ages'))
    writeFieldToXml(xmlFile, "Mechanic", game.getInfoByCategoryName('Mechanic'))
    writeFieldToXml(xmlFile, "Expansion", game.getInfoByCategoryName('Expansion'))
    writeFieldToXml(xmlFile, "Website", game.getInfoByCategoryName('Website'))
    writeFieldToXml(xmlFile, "Alternate Names", game.getInfoByCategoryName('Alternate Names'))
    writeFieldToXml(xmlFile, "Expansion", game.getInfoByCategoryName('Expansion'))
    writeFieldToXml(xmlFile, "Artist", game.getInfoByCategoryName('Artist'))
    writeFieldToXml(xmlFile, "Publisher", game.getInfoByCategoryName('Publisher'))
    writeFieldToXml(xmlFile, "Honors", game.getInfoByCategoryName('Honors'))
    writeFieldToXml(xmlFile, "Description", game.getDescription())

    xmlFile.write('</doc>\n\n')
    print str(i) + ' entry has been processed'

xmlFile.write('</add>')
xmlFile.close()
