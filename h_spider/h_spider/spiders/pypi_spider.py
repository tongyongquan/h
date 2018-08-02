# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import datetime
import dateparser
from scrapy import Request
from scrapy.utils.request import request_fingerprint
from urllib.parse import urlparse
from ..items import HSpiderItem

class PypiSpiderSpider(scrapy.Spider):
    name = 'pypi_spider'
    # 逻辑没问题但allowed_domains设错可能导致爬虫无法请求一些页面!/
    allowed_domains = ['pypi.org']

    def __init__(self, question='hack', *args, **kwargs):
        super(PypiSpiderSpider, self).__init__(*args, **kwargs)
        self.question = question
        self.start_urls = ['https://pypi.org/search/?q=%s' % question]

    custom_settings = {
        "MONGO_COLLECTION": "news",
        # "SPIDER_MIDDLEWARES": {
        #     'kete_spider.middlewares.CrawlOnceMiddleware': 100,
        # },
        # "DOWNLOADER_MIDDLEWARES": {
        #     'kete_spider.middlewares.CrawlOnceMiddleware': 50,
        # },
        # "ITEM_PIPELINES": {
        #     'kete_spider.pipelines.news_pipeline.NewsPipeline': 300
        # }
    }

    # 打开start_url的scrapy shell解析列表页
    def parse(self, response):
        link_lists = response.xpath('//ul[@class="unstyled"]/li/a/@href').extract()
        for link in link_lists:
            url = response.urljoin(link)
            # 打印验证链接列表准确性
            print(url)
            yield Request(url=url, callback=self.parse_detail)
        next_page_node = response.xpath('//div[@class="button-group button-group--pagination"]/a[text()="Next"]/@href')
        if next_page_node:
            next_page_url = response.urljoin(next_page_node.extract_first())
            # 打印验证下一页列表准确性
            print(next_page_url)
            yield Request(url=next_page_url, callback=self.parse)

    # 退出列表页的scrapy shell 先验证是否爬取了所有链接,scrapy crawl **spider_name**

    # 打开爬到的链接scrapy shell 解析详情
    def parse_detail(self, response):
        title = response.xpath('//h1[@class="package-header__name"]/text()').extract_first().strip()
        content = ' '.join([x.strip() for x in response.xpath('//div[@id="description"]//text()').extract()])
        html_content = response.xpath('//div[@id="description"]').extract_first()
        project_link = response.xpath('//div[@class="sidebar-section"]/a/@href').extract_first()
        # 只要能view出来就不需要模拟操作,查看response的body(未被dom的)才是xpath真正能操作的,找到接口
        github_info_api = response.xpath('//div[@class="github-repo-info hidden"]/@data-url').extract_first()
        try:
            res = requests.get(github_info_api)
            jd = json.loads(res.text)
            info = {
                'author': jd['owner']['login'],
                'avatar_url': jd['owner']['avatar_url'],
                "created_at": dateparser.parse(jd["created_at"]),
                "updated_at": dateparser.parse(jd["updated_at"]),
                "forks_count": jd["forks_count"],
                "stargazers_count": jd["stargazers_count"],
                "watchers_count": jd["watchers_count"]
            }
        except Exception as e:
            print(e)
            info = {}

        print(title, content, html_content, project_link, info)
        item = HSpiderItem()
        item['spider_name'] = self.name
        item['domain'] = urlparse(response.url).netloc
        item['url'] = response.url
        item['url_hash'] = request_fingerprint(response.request)
        item['crawl_date'] = datetime.datetime.now()

        item['question'] = self.question
        item['title'] = title
        item['content'] = content
        item['html_content'] = html_content
        item['project_link'] = project_link
        item['info'] = info
        yield item
