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
from loader import QiitaCalendarLoader


class QiitaCalendarSpider(scrapy.Spider):
    name = "qiita_calendar"
    allowed_domains = ["qiita.com"]
    start_urls = ["http://qiita.com/advent-calendar/2016/calendars"]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        for href in response.css('table.table.adventCalendarList tbody tr'):
            calendar_title = href.css('td.adventCalendarList_calendarTitle a::text').extract_first()
            calendar_url = href.css('td.adventCalendarList_calendarTitle a::attr(href)').extract_first()
            calendar_attendees = href.css(
                'td.adventCalendarList_progress span.adventCalendarList_recruitmentCount::text').extract_first()

            yield {
                'calendar_title': calendar_title,
                'calendar_url': response.urljoin(calendar_url),
                'calendar_attendees': calendar_attendees
            }

            for page in response.css('li.hidden-xs a'):
                next_page = page.css('::attr(href)').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)


class QiitaArticleSpider(scrapy.Spider):
    name = "qiita_article"
    allowed_domains = ["qiita.com"]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def start_requests(self):
        qiita_calendars = QiitaCalendarLoader()
        for url in qiita_calendars.urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        href = response.css('ul.list-inline')
        calendar_category_name = href.css(
            'div.label[class*="adventCalendarJumbotron_label-"] a::text').extract_first()
        calendar_category_url = href.css(
            'div.label[class*="adventCalendarJumbotron_label-"] a::attr(href)').extract_first()
        calendar_participants = href.css('li[title="Participants"]::text').extract_first()
        calendar_likes = href.css('li[title="Likes"]::text').extract_first()
        calendar_subscribers = href.css('li[title="Subscribers"]::text').extract_first()

        calendar_owner_url = response.css('p.adventCalendarJumbotron_owner a::attr(href)').extract_first()
        calendar_owner = response.css('p.adventCalendarJumbotron_owner a::text').extract_first()

        if calendar_participants is not None:
            calendar_participants = calendar_participants.strip()

        if calendar_likes is not None:
            calendar_likes = calendar_likes.strip()

        if calendar_subscribers is not None:
            calendar_subscribers = calendar_subscribers.strip()

        if calendar_category_url is not None:
            calendar_category_url = response.urljoin(calendar_category_url)

        if calendar_owner_url is not None:
            calendar_owner_url = response.urljoin(calendar_owner_url)

        if calendar_owner is not None:
            calendar_owner = calendar_owner.strip()

        yield {
            'calendar_url': response.url,
            'type': 'calendar',
            'calendar_category_name': calendar_category_name,
            'calendar_category_url': calendar_category_url,
            'calendar_participants': calendar_participants,
            'calendar_likes': calendar_likes,
            'calendar_subscribers': calendar_subscribers,
            'calendar_owner': calendar_owner,
            'calendar_owner_url': calendar_owner_url
        }

        for href in response.css('div.adventCalendarItem'):
            date = href.css("div.adventCalendarItem_date::text").extract_first()
            author_url = href.css("div.adventCalendarItem_author a::attr(href)").extract_first()
            author = href.css("div.adventCalendarItem_author a::text").extract_first()
            article_url = href.css("div.adventCalendarItem_entry a::attr(href)").extract_first()
            article_title = href.css("div.adventCalendarItem_entry a::text").extract_first()

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
