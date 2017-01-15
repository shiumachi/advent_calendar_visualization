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
import json
from urllib.parse import urlencode
from loader import QiitaCalendarLoader, AdventarCalendarLoader, QiitaArticleLoader, AdventarArticleLoader


class HatenaBookmarkSpider(scrapy.Spider):
    name = "hatenabookmark"
    allowed_domains = ["qiita.com", "www.adventar.org"]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    entry_point = 'http://api.b.st-hatena.com/entry.counts'
    max_url = 50  # max url counts which Hatena Bookmark API allows

    def urls(self, loader):
        url_set = set()
        for url in loader.urls():
            url_set.add(url)
            if len(url_set) < self.max_url:
                continue

            req_url = self.entry_point + '?' + urlencode(list(map(lambda x: ('url', x), url_set)))
            yield req_url
            url_set = set()

    def start_requests(self):

        loaders = [
            QiitaCalendarLoader,
            AdventarCalendarLoader,
            QiitaArticleLoader,
            AdventarArticleLoader
        ]
        for loader in loaders:
            for url in self.urls(loader()):
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield json.loads(response.text)
