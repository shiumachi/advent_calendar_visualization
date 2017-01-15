# Copyright 2017 Sho Shimauchi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import scrapy
from loader import AdventarCalendarLoader


class AdventarCalendarSpider(scrapy.Spider):
    name = "adventar_calendar"
    allowed_domains = ["www.adventar.org"]
    start_urls = ["http://www.adventar.org/calendars?year=2016"]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        for href in response.css('div.mod-calendarList li'):
            calendar_title = href.css('div.mod-calendarList-title a::text').extract_first()
            calendar_url = href.css('div.mod-calendarList-title a::attr(href)').extract_first()
            calendar_attendees = href.css(
                'div.mod-calendarIndicator-value::attr(data-count)').extract_first()

            if calendar_url is not None:
                calendar_url = response.urljoin(calendar_url)

            yield {
                'calendar_title': calendar_title,
                'calendar_url': calendar_url,
                'calendar_attendees': calendar_attendees
            }


class AdventarArticleSpider(scrapy.Spider):
    name = "adventar_article"
    allowed_domains = ["www.adventar.org"]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def start_requests(self):
        adventar_calendars = AdventarCalendarLoader()
        for url in adventar_calendars.urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        calendar_owner_url = response.css('div.mod-calendarHeader-meta p a::attr(href)').extract_first()
        calendar_owner = response.css('div.mod-calendarHeader-meta p a span::text').extract_first()

        if calendar_owner_url is not None:
            calendar_owner_url = response.urljoin(calendar_owner_url)

        if calendar_owner is not None:
            calendar_owner = calendar_owner.strip()

        yield {
            'calendar_url': response.url,
            'type': 'calendar',
            'calendar_owner': calendar_owner,
            'calendar_owner_url': calendar_owner_url
        }

        for href in response.css('table.mod-entryList tr'):
            date = href.css('th.mod-entryList-date::text').extract_first()
            author_url = href.css('td.mod-entryList-user a::attr(href)').extract_first()
            author = href.css('td.mod-entryList-user span::text').extract_first()
            article_url = href.css('td.mod-entryList-body div.mod-entryList-url a::attr(href)').extract_first()
            article_title = href.css('td.mod-entryList-body div.mod-entryList-title::text').extract_first()

            if author is not None:
                author = author.strip()

            if author_url is not None:
                author_url = response.urljoin(author_url)

            if article_title is not None:
                article_title = article_title.strip()

            yield {
                'calendar_url': response.url,
                'type': 'article',
                'date': date,
                'author_url': author_url,
                'author': author,
                'article_url': article_url,
                'article_title': article_title
            }
