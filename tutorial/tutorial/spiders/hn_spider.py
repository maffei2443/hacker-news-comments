import datetime as dt
import scrapy

from tutorial.spiders.helper import ParseDateApproximate
import pymongo

from bs4 import BeautifulSoup

class HNSpyder(scrapy.Spider):
    
    name = 'comments'

    def __init__(self, name=None, **kwargs):
        super(HNSpyder, self).__init__(name=name, **kwargs)
        # Will be set by `MongoPipeline`
        self.min_required_id = None
        self.mail = None
        self.debug = kwargs.get('debug', False)


    def start_requests(self):
        urls = ['https://news.ycombinator.com/newcomments']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)



    def parse(self, response):
        selectors = response.css('tr.athing')
        ids = []
        lis = []
        today = dt.date.today()
        for selec in selectors:
            comm_selec = selec.css('span[class="commtext c00"]')
            date_selec = selec.css('span[class="age"] a').xpath('text()')
            id_ = int(selec.xpath('@id').get())
            text = BeautifulSoup(comm_selec.get()).text
            parent_id = selec.css('span.par a').xpath('@href').re_first(r'\d+')
            by = selec.css('a.hnuser').xpath('@href').re_first(r'id=(.+)')
            date = ParseDateApproximate.parse(date_selec.get(), today=today)
            links = [i.attrib['href'] for i in selec.css('div.comment a')]
            # Actually the truly information about time is not available,
            # but an `order` can be obtained exploiting the fact
            # `id` only rises through time.

            item = dict(
                text=text,
                parent=int(parent_id),
                by=by,
                id=id_,
                date=date,
                links=links,
            )
            yield item        
            ids.append(id_)
        if self.debug:
            print("min_required_id < min(ids) ? {} < {} ".format(self.min_required_id, min(ids)))
            input()
        if self.min_required_id < min(ids):
            next_url = response.urljoin(response.css('a.morelink').attrib['href'])
            print("NEXT_URL: {}".format(next_url))
            yield scrapy.Request(url=next_url, callback=self.parse)
