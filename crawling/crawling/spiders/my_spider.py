import scrapy
from ..items import CrawlingItem
import w3lib.html


class ArticleSpider(scrapy.Spider):
    name = "article"
    start_urls = [
        'https://nbs.sk/en/news/s-tatement-from-the-27th-meeting-of-the-bank-board-of-the-nbs/',
        'https://nbs.sk/en/news/report-on-economic-development-in-may-2010-summary/',
        'https://nbs.sk/en/news/statement-from-the-24th-meeting-of-the-bank-board-of-nbs/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-april-2010/',
        'https://nbs.sk/en/news/statement-from-the-22nd-meeting-of-the-bank-board-of-nbs/',
        'https://nbs.sk/en/news/statement-from-the-21st-meeting-of-the-bank-board-of-the-nbs-2/',
        'https://nbs.sk/en/news/statement-from-the-20th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/meeting-of-the-nbs-management-representatives-of-banks-and-investment-firms/',
        'https://nbs.sk/en/news/statement-from-the-18th-meeting-of-the-bank-board-of-narodna-banka-slovenska/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-march-2010/',
        'https://nbs.sk/en/news/statement-from-the-17th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/statement-from-the-14th-meeting-of-the-bank-board-of-the-nbs-2/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-february-2010/',
        'https://nbs.sk/en/news/statement-from-the-11th-meeting-of-the-bank-board-of-the-nbs-4/',
        'https://nbs.sk/en/news/statement-from-the-10th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/statement-from-the-9th-meeting-of-the-bank-board-of-the-nbs-3/',
        'https://nbs.sk/en/news/statement-from-the-8th-meeting-of-the-bank-board-of-the-nbs-2/',
        'https://nbs.sk/en/news/summary-report-on-economic-development-in-january-2010/',
        'https://nbs.sk/en/news/nbs-warning-regarding-unauthorised-activity-of-the-trading-company-plus500-ltd/',
        'https://nbs.sk/en/news/statement-from-the-44th-meeting-of-the-bank-board-of-the-nbs-2/',
    ]

    def parse(self, response, **kwargs):
        item = CrawlingItem()

        date =  response.css("div.nbs-post__date::text").get()
        name = response.css("h1.headline::text").get()
        link = response.request.url
        labels = response.css("div.label--sm::text").get()
        selectors = response.css("p")
        content = ''
        for selector in selectors:
            text = selector.get()
            text = w3lib.html.remove_tags(text)
            if "<p>" in text:
                text = text.replace("<p>", "")
            if "</p>" in text:
                text = text.replace("</p>", "")
            if "<strong>" in text:
                text = text.replace("<strong>", "")
            if "</strong>" in text:
                text = text.replace("</strong>", "")
            if "<br>" in text:
                text = text.replace("<br>", "")
            if "</br>" in text:
                text = text.replace("</br>", "")
            if "Internet:" in text:
                break

            content += text

        item["date"] = date
        item["name"] = name
        item["link"] = link
        item["labels"] = labels
        item["content"] = content

        yield item
