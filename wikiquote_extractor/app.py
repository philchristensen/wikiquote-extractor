import sys
import logging
import urlparse
import urllib2
import re

logging.basicConfig(level=logging.INFO)

log = logging.getLogger("wikiquote")

def process_season_quotes(season_no, url):
    html_doc = urllib2.urlopen(url).read()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_doc)
    
    content = soup.find('div', id="mw-content-text")
    for node in content.find_all('h3'):
        episode = node.find('span', class_="mw-headline")
        episode_name = episode.string
        
        for next_node in node.next_siblings:
            print '%'
            if(next_node.name == 'dl'):
                for quote in next_node.find_all('dd'):
                    quote_line = ''.join([x if x.startswith(':') else ' ' + x for x in list(quote.stripped_strings)])
                    print quote_line.encode('utf8')
                source = '        -- "%s", season %s' % (episode_name, season_no)
                print source.encode('utf8')
            elif(next_node.name == 'h3'):
                break

def main(args=sys.argv):
    season_list_url = "http://en.wikiquote.org/wiki/The_Simpsons"
    
    req = urllib2.urlopen(season_list_url)
    html_doc = req.read()
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_doc)
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if(href is None):
            continue
        match = re.match(r'(.*?)/Season_(\d+)$', href, re.I)
        if(match):
            season_no = int(match.group(2))
            if(season_no > 12):
                continue
            season_page_url = urlparse.urljoin(season_list_url, href)
            process_season_quotes(season_no, season_page_url)

if(__name__ == '__main__'):
    main()