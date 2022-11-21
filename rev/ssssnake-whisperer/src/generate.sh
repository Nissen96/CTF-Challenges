#!/bin/bash
python3 reveal.py > reveal.dis

# Transform slightly to throw off automated tools
sed -i "s/ >>/>>>/g" reveal.dis
sed -i -r "s/^( +[[:digit:]]+)  /\1: /g" reveal.dis
