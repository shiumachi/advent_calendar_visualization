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
from os.path import dirname, realpath, join

FILE_DIR = dirname(realpath(__file__))
DATA_DIR = join(FILE_DIR, '../data')
SOURCE_JSON = join(DATA_DIR, 'hatenabookmark.json')
TARGET_CSV = join(DATA_DIR, 'hatenabookmark_converted.csv')


with open(SOURCE_JSON) as f:
    data = json.loads(f.read())

f = open(TARGET_CSV, 'w')
f.write("url,count\n")
for d in data:
    for (url, count) in d.items():
        f.write('"{0}",{1}\n'.format(url, count))

f.close()
