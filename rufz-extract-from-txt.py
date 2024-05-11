#!/bin/env python3

import sys
import re

script, file = sys.argv
text = [l.strip('\n\r') for l in open(file, "r").readlines()]
text = [string if not string.startswith("Seite ") else " " for string in text]
text = "".join(text)
text = text.replace(", ", ",").replace("; ", ";")

# call sign
startP = "D[A-Z0-9]{4,5}"
# class, name{[,;] street; town{, street; town}}
midP = (r"(?P<class>[AE])[,;]?" +
        "(?P<name>.*?)" +
        "(?P<addr>[,;].*?)?")
#midP = r"(.*?)"
pattern = re.compile(
    r"(?P<callsign>" + startP + ")," +      # call sign
    # class, name{; street; town{, street; town}}
    midP +
    r"(?=" + startP + ",|\Z)",  # end as look-ahead, or end of text "\Z"
    re.DOTALL)

print("callsign,class,name,addr1,addr2")

for match in pattern.finditer(text):
    # print(match)
    # continue

    # call sign
    print(f"{match['callsign']},", end="")

    # class, name{; street; town{, street; town}}
    # class
    print(f"{match['class']},", end="")
    # name
    print(f"{match['name'].strip()},", end="")
    # addresses
    if match['addr']:
        addr = match['addr'].strip(",; ").split(",")
        # street, town
        print(f"{addr[0]}," if addr[0] else "n/a,", end="")
        # street, town
        print(f"{addr[1]}" if len(addr) > 1 else "n/a")
    else:
        print("n/a,n/a")
