# System Requirement

## Python Library

```
$ pip install scrapy
```

## Pentaho Data Integration (PDI)

Download PDI from http://community.pentaho.com/projects/data-integration/


# How to use

## Collect Calendar Lists

```
$ scrapy crawl qiita_calendar -o advent_calendar/data/qiita_calendar.json
$ scrapy crawl adventar_calendar -o advent_calendar/data/adventar_calendar.json
```

## Collect Calendar Pages

Make Sure the previous part is finished and the calendar json files are created.

```
$ scrapy crawl qiita_article -o advent_calendar/data/qiita_article.json
$ scrapy crawl adventar_article -o advent_calendar/data/adventar_article.json
```

## Get Hatena Bookmark counts

```
$ scrapy crawl hatenabookmark -o advent_calendar/data/hatenabookmark.json
```

## Data Preparation for ETL

```
$ python advent_calendar/spiders/splitter.py
$ python advent_calendar/process/hatenabookmark_json_transform.py
```

## Run ETL job in PDI

- Start `Data Integration` application.
- Choose `Run` and set `PROJECT_HOME` variable to the directory where you cloned this repository.
- If there is no error on job completion, you'll get refined data under `advent_calendar/refined` directory.
