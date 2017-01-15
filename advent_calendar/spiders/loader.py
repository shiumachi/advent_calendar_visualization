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

import json
import os.path
import logging


logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)-4.4s [%(name)s] %(message)s')

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data')


class BaseLoader(object):
    data = None
    file_path = None

    def __init__(self):
        path = os.path.join(DATA_DIR, self.file_path)
        if not os.path.exists(path):
            logging.warn("file {} is not found. This can be fine when you run this crawler first time.".format(self.file_path))
            return
        with open(path) as f:
            raw_data = f.read()
        self.data = json.loads(raw_data)


class QiitaCalendarLoader(BaseLoader):
    file_path = 'qiita_calendar.json'

    def urls(self):
        for records in self.data:
            yield records['calendar_url']


class AdventarCalendarLoader(BaseLoader):
    file_path = 'adventar_calendar.json'

    def urls(self):
        for records in self.data:
            yield records['calendar_url']


class QiitaArticleLoader(BaseLoader):
    file_path = 'qiita_article.json'

    def urls(self):
        for records in self.data:
            if records['type'] == 'calendar':
                continue
            if records['article_url'] is None:
                continue
            yield records['article_url']

    def records(self):
        for record in self.data:
            yield record


class AdventarArticleLoader(BaseLoader):
    file_path = 'adventar_article.json'

    def urls(self):
        for records in self.data:
            if records['type'] == 'calendar':
                continue
            if records['article_url'] is None:
                continue
            yield records['article_url']

    def records(self):
        for record in self.data:
            yield record
