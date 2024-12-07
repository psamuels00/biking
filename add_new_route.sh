#!/bin/sh

src/show_stats.py && \
git add images output && \
git commit -m "add data" && \
git push
