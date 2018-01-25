#!/bin/bash

set -e

. venv/bin/activate
cd claimreview

scrapy crawl faktisk
scrapy crawl wp
scrapy crawl claimreview

