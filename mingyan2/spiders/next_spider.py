# -*- coding: utf-8 -*-
import scrapy
import sys

class NextSpiderSpider(scrapy.Spider):
    name = "nextSpider"
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        mingyan = response.css('div.quote')

        for v in mingyan:
            text = v.css('.text::text').extract_first()
            author = v.css('.author::text').extract_first()
            tags = v.css('.tags .tag::text').extract()
            tags = ','.join(tags) #数组转化为字符串

            #每个作者的内容存储为一个txt文本
            filename = '%s-语录.txt' % author

            with open(filename,"a+") as f:
                f.write(text)
                f.write('\n')
                f.write('标签：'+tags)
                f.write('\n--------------\n')
                f.close()
        #判断下一页是否存在，存在继续scrapy
        next_page = response.css('li.next a::attr(href)').extract_first()
        #self.log('当前页：%s' % next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            #self.log('当前url：%s' % next_page)
            yield scrapy.Request(next_page,callback=self.parse)



