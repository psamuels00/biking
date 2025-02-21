#!/bin/sh

publish() {
    rsync -av --exclude=formula/ --exclude=legend/ output/ docs/
    rsync -av src/pages/index/index.html docs/

    git add docs
    git commit -m "publish updates"
}

publish
