#!/usr/bin/env bash

scrapy crawl $1 -s LOG_LEVEL="DEBUG" -s TEST_MODE=False
