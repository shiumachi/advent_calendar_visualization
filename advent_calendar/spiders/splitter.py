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
import logging
from loader import QiitaArticleLoader, AdventarArticleLoader

logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)-4.4s [%(name)s] %(message)s')


class ArticleJsonSplitter(object):
    calendars = []
    articles = []
    calendar_json_file = None
    article_json_file = None
    loader = None

    def __init__(self, file_dir):
        self.calendar_json_file = file_dir + self.calendar_json_file
        self.article_json_file = file_dir + self.article_json_file

    def split(self):
        for record in self.loader.records():
            if record['type'] == 'calendar':
                logging.info("marked as calendar: {}".format(record))
                self.calendars.append(record)
            elif record['type'] == 'article':
                logging.info("marked as article: {}".format(record))
                self.articles.append(record)
            else:
                logging.warn("this record has no type: {}".format(record))

    def dump(self):
        logging.info("dump to json files...")

        with open(self.calendar_json_file, 'w') as f:
            f.write(json.dumps(self.calendars))

        with open(self.article_json_file, 'w') as f:
            f.write(json.dumps(self.articles))

        logging.info("dump finished.")


class QiitaArticleJsonSplitter(ArticleJsonSplitter):
    calendar_json_file = '/../data/qiita_calendar_details.json'
    article_json_file = '/../data/qiita_article_details.json'
    loader = QiitaArticleLoader()


class AdventarArticleJsonSplitter(ArticleJsonSplitter):
    calendar_json_file = '/../data/adventar_calendar_details.json'
    article_json_file = '/../data/adventar_article_details.json'
    loader = AdventarArticleLoader()


def main():
    from os.path import dirname, realpath
    file_dir = dirname(realpath(__file__))

    splitter = QiitaArticleJsonSplitter(file_dir)
    splitter.split()
    splitter.dump()

    splitter = AdventarArticleJsonSplitter(file_dir)
    splitter.split()
    splitter.dump()


if __name__ == '__main__':
    main()
