#!/bin/bash

set -e
set -x

. venv/bin/activate
cd claimreview

for spider in claimreview/spiders/*.py
do
  spider_name=$(basename $spider .py)

  if [[ $spider_name != __* ]]; then
    scrapy crawl $spider_name
  fi
done

