tryagain () {
    src/analyze.py "$@" && rsync -qav --exclude=formula/ --exclude=legend/ output/ docs/
}

