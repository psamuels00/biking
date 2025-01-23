#!/bin/sh

# crop to content and add left margin to images
crop_and_indent() {
    cd $1
    for file in *.png; do
         magick $file -trim -bordercolor white -border 72x0 +repage $file
    done
}

src/mk_formula_images.py
crop_and_indent output/formula
