import datetime as dt
import scrapy

from tutorial.spiders.helper import ParseDateApproximate

class HNSpyder(scrapy.Spider):
    name = 'comments'


    start_urls = [
        'https://news.ycombinator.com/newcomments'
    ]
  

    def parse(self, response):
        selectors = response.css('tr.athing')
        ids = []
        lis = []
        today = dt.date.today()
        for selec in selectors:
            comm_selec = selec.css('span[class="commtext c00"]')
            date_selec = selec.css('span[class="age"] a').xpath('text()')

            id_ = selec.xpath('@id').get()
            text = ''.join(comm_selec.xpath('text()').getall())
            parent_id = selec.css('span.par a').xpath('@href').re_first(r'\d+')
            by = selec.css('a.hnuser').xpath('@href').re_first(r'id=(.+)')
            date = ParseDateApproximate.parse(date_selec.get(), today=today)
            # Actually the truly information about time is not available,
            # but an `order` can be obtained exploiting the fact
            # `id` only rises through time.
            order = int(id_)
            item = dict(
                text=text,
                parent=parent_id,
                by=by,
                id=id_,
                date=date,
            )
            # print(item)
            ids.append(order)
        next_url = response.urljoin(response.css('a.morelink').attrib['href'])
        print("NEXT_URL: {}".format(next_url))
        
        yield scrapy.Request(url=next_url, callback=self.parse)
        return lis