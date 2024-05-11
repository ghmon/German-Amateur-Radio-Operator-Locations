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
midP = r"(([AE])[,;]?(.*?)([,;].*?)?)"
#midP = r"(.*?)"
pattern = re.compile(
    r"(" + startP + ")," +      # call sign
    # class, name{; street; town{, street; town}}
    midP +
    r"(?=" + startP + ",|\Z)",  # end as look-ahead, or end of text "\Z"
    re.DOTALL)

print("callsign,class,name,addr1,addr2")

matches = re.findall(pattern, text)

for match in matches:
    # print(match)
    # continue

    # call sign
    print(f"{match[0]},", end="")

    # class, name{; street; town{, street; town}}
    # class
    print(f"{match[2]},", end="")
    # name
    print(f"{match[3].strip()},", end="")
    # addresses
    if match[4]:
        addr = match[4].strip(",; ").split(",")
        # street, town
        print(f"{addr[0]}," if addr[0] else "n/a,", end="")
        # street, town
        print(f"{addr[1]}" if len(addr) > 1 else "n/a")
    else:
        print("n/a,n/a")
