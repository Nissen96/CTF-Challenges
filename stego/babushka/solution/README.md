# Writeup


This steganography challenge focuses on file carving. The provided ZIP file contains 6 images where one is of a Matryoshka doll. This image file hides another nested ZIP-file after the image data, again containing 6 new images with a (now smaller) Matryoshka doll. This continues recursively 10 times and the ZIP-file hidden in the smallest doll contains the flag file.

At each level, all image files can be checked for hidden files with `binwalk *`, and the hidden file extracted with `binwalk -e *`. This can be automated with the `-M/--matryoshka` flag, which ensures `binwalk` scans and extracts recursively, together with `-d/--depth 20` to ensure it doesn't stop at the default depth of 8.

Solution one-liner:

```bash
binwalk -e --matryoshka --depth 20 Бабушка.zip && find . -name flag.txt -exec cat {} \;
```