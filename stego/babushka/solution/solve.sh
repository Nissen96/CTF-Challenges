#!/bin/bash
binwalk -e --matryoshka --depth 20 Бабушка.zip && find . -name flag.txt -exec cat {} \;
