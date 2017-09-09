from PttWebCrawler.crawler import *

c = PttWebCrawler(as_lib=True)
c.parse_articles(1, 25000, 'Gossiping')
