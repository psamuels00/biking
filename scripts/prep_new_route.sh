#!/bin/sh

process_route() {
    local num_files=`ls images/Screenshot* 2> /dev/null | wc -l`

    if [ $num_files = 1 ]; then
        local ymd=`date +%Y%m%d`
        local in_file=`ls images/Screenshot*`
        local miles=`printf %02d $num_miles`
        local out_file="images/bike-route-$ymd-${miles}mi.png"

        magick "$in_file" -crop +0+240 $out_file && \
        rm "$in_file" && \
        echo "Screenshot file $in_file replaced by $out_file." && \
        src/show_stats.py
    elif [ $num_files = 0 ]; then
        echo "Screenshot file not found."
    else
        echo "Multiple Screenshot files found."
    fi
}

num_miles=$1

if [ -z "$num_miles" ]; then
    echo "usage: $1 <num_miles>"
    exit 1
fi

process_route $num_miles

