import re
import datetime as dt
import scrapy

from tutorial.spiders.helper import ParseDateApproximate
print(__name__)

class HNSpyder(scrapy.Spider):
    name = 'comments'

    def _extract_id(self, s):
        return re.search(r'id=(.+?)"', s).group(1)

    def start_requests(self):
        urls = [
            'https://news.ycombinator.com/newcomments'
        ]
        self.today = dt.date.today()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        selectors = response.css('tr.athing')
        comm_selectors = response.xpath('//span[contains(@class, "commtext c00")]')
        date_selectors = response.xpath('//span[@class="age"]/a/text()')
        ids = []
        lis = []
        for selec, comm_selec, date_selec in zip(selectors, comm_selectors, date_selectors):
            text = ''.join([i.get() for i in comm_selec.xpath('text()')])
            parent_id = self._extract_id(selec.css('span.par').extract_first())
            by = selec.css('a.hnuser')[0].attrib['href'].split('id=')[1]
            id_ = selec.attrib['id']
            print('CREATION DATE:', date_selec.get())
            print("TODAY:", self.today)            
            date = ParseDateApproximate.parse(date_selec.get(), today=self.today)
            print("CREATION DATE:", date)
            # Actually the truly information about time is not available,
            # but an `order` can be obtained exploiting the fact
            # `id` only rises through time.
            order = int(id_)
            lis.append(dict(
                text=text,
                parent=parent_id,
                by=by,
                id=id_,
                date=date,
            ))
            input(lis[-1])
            # So it is possible to decide whether to
            # get the next page of comments or not
            ids.append(order)
        return lis