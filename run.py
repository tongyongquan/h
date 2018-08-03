__author__ = 'Administrator'
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process = CrawlerProcess(get_project_settings())
        process.crawl(sys.argv[1])
        process.start()
    else:
        print('ERROR:miss spider name!')

