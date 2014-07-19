#!/usr/bin/env python
from urllib import urlopen
from StringIO import StringIO
import gzip
from bs4 import BeautifulSoup
import sys
# import codecs
import cgi
import itertools
import argparse
url = 'http://boardgamegeek.com/boardgame/'


class BoardGameParser:

    def __init__(self, gameUrl):
        print "Conecting to: " + gameUrl+" .."
        response = urlopen(gameUrl)
        if (response.info()
                    .get('Content-Encoding')) == 'gzip':
            print "Ungzipping.."
            buffer = StringIO(response.read())
            html_doc = gzip.GzipFile(fileobj=buffer)
            buffer.close
        else:
            html_doc = response.read()

        print "Parsing..."
        self.soup = BeautifulSoup(html_doc)

    def getNameOfGame(self):
        if self.soup.find('b') is None:
            return ''
        elif (self.soup
                  .b
                  .text) == 'Error: Could not view GeekItem':
            return ''
        else:
            return self.soup.h1.span.text

    def getInfoByCategoryName(self, categoryName):
        if (self.soup
                .find('b')) is None:
            return ''
        elif (self.soup
                  .b
                  .text) == 'Error: Could not view GeekItem':
            return ''
        elif (self.soup
                  .find('table', class_='geekitem_infotable')
                  .find('b', text=categoryName)) is None:
            return ''
        else:

            newsoup = (self.soup
                           .find('table', class_='geekitem_infotable')
                           .find('b', text=categoryName)
                           .find_next('td').prettify())
            newsoup = BeautifulSoup(newsoup)

            if newsoup.find('a') is None:
                return (newsoup.text
                               .strip()
                               .replace('\n', '')
                               .replace('\t', ''))
            else:
                result = ''
                for text in newsoup.find_all('a'):
                    result = result + (text
                                       .text
                                       .strip()
                                       .replace('\n', '')
                                       .replace('\t', '') + ', ')
                return result

    def getDescription(self):
        if (self.soup
                .find('b')) is None:
            return ''
        elif (self.soup
                  .b
                  .text) == 'Error: Could not view GeekItem':
            return ''
        elif (self.soup
                  .find('div', class_='wiki')) is None:
            return ''
        else:
            return ('\n'.join(str(self.soup
                                      .find('div', class_='wiki')
                                      .text)
                              .split('\n')[1:-1])
                        .replace('\n', '\\n'))


def writeFieldToXml(xmlFile, list_of_names, list_of_values):
    if len(list_of_names) == len(list_of_values):
        for name, value in itertools.izip(list_of_names, list_of_values):
            string = (' <field name=\"' +
                      name +
                      '\">' +
                      cgi.escape(str(value)) +
                      '</field>\n')
            xmlFile.write(string)
    else:
        raise ValueError('List of names does not'
                         'correspond to the list of values')


def main(argv):
    parser = argparse.ArgumentParser(description='get items from ' +
                                     url +
                                     ' and output them to an xml file')
    parser.add_argument('-o', nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output XML file')
    # output = 'boardgamegeek_1-5k.xml'
    output = parser.parse_args(argv)
    xmlFile = output.o

    xmlFile.write('<add>\n')

    for i in xrange(1, 5000):
        gurl = url + str(i)

        xmlFile.write('<doc>\n')
        game = BoardGameParser(gurl)

        print "Writing to file.."
        writeFieldToXml(xmlFile,
                        ["id",
                         "name",
                         "category",
                         "designer",
                         "year_published",
                         "numder_of_players",
                         "playing_time",
                         "mfg_suggested_ages",
                         "mechanic",
                         "expansion",
                         "website",
                         "alternate_names",
                         "artist",
                         "publisher",
                         "honors",
                         "description"],
                        [str(i),
                         game.getNameOfGame(),
                         game.getInfoByCategoryName('Category'),
                         game.getInfoByCategoryName('Designer'),
                         game.getInfoByCategoryName('Year Published'),
                         game.getInfoByCategoryName('# of Players'
                                                    .encode('utf-8')),
                         game.getInfoByCategoryName('Playing Time'),
                         game.getInfoByCategoryName('Mfg Suggested Ages'),
                         game.getInfoByCategoryName('Mechanic'),
                         game.getInfoByCategoryName('Expansion'),
                         game.getInfoByCategoryName('Website'),
                         game.getInfoByCategoryName('Alternate Names'),
                         game.getInfoByCategoryName('Artist'),
                         game.getInfoByCategoryName('Publisher'),
                         game.getInfoByCategoryName('Honors'),
                         game.getDescription()])

        xmlFile.write('</doc>\n\n')
        print str(i) + ' entry has been processed'

    xmlFile.write('</add>')
    xmlFile.close()


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    main(sys.argv[1:])
