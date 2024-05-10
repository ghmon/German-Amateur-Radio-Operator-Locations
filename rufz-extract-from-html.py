#!/bin/env python3

import sys
import re

import html

script, file = sys.argv
text = "".join([l.strip('\n\r') for l in open(file, "r").readlines()])

pattern = re.compile(r"<b>(D[A-Z0-9]{4,5})" +      # call sign
                     r"(.*?)" +                   # non-greedy all chars until
                     r"<b>(?=D[A-Z0-9]{4,5}|\Z)",  # end as look-ahead, or end of text "\Z"
                     re.DOTALL)

print("callsign,class,name,street,town")

text = text.replace("</div></div>", "")
text = text.replace('<div style="page-break-before:always; page-break-after:always"><div><p>', "")

matches = re.findall(pattern, text)

for match in matches:
    # call sign
    print(f"{match[0]},", end="")

    # class, name, address
    # cleanup
    desc = match[1].strip().replace("\n", " ").replace("\r", " ")
    desc = desc.replace("<b>", "").replace("</b>", "")
    desc = desc.replace("<p>", "").replace("</p>", " ")
    desc = desc.strip(", ")

    desc = html.unescape(desc)
    desc = desc.split(", ")
    # class
    print(f"{desc[0]},", end="")
    desc = desc[1].split(";")
    # name
    print(f"{desc[0]},", end="")
    # street
    print(f"{desc[1].strip()}," if len(desc) > 1 else "n/a,", end="")
    # town
    print(f"{desc[2].strip()}" if len(desc) > 2 else "n/a")
    # # betriebsort
    # print(f"{desc[3]}" if len(desc) > 3 else "n/a")
