# German-Amateur-Radio-Operator-Locations

Convert amateur radio operator addresses from the Bundesnetzagentur to geocoded file with latitude/longitude position
=====================

Requirements:

- Java JRE (used: openjdk 17.0.10 2024-01-16)
- Python3 (used: Python 3.10.12)
- Python module "geopy": pip3 install geopy (used 2.3.0)
- Apache PDFBox (used 2.0.31)

Tested on Ubuntu 22.04 LTS.

Limitations:

* not all addresses are found by the locator

* not all entries (a few) in the source file from the
  Bundesnetzagentur have addresses

So currently you get 60000+ address locations out of 69000+ call signs.

The project is inspired by
[CallmapGermany](https://github.com/df8oe/CallmapGermany) from Ulrich
Thiel, but uses no code from there.

* Download PDF with addresses of amateur radio operators from the Bundesnetzagentur

["Verzeichnis der zugeteilten deutschen Amateurfunkrufzeichen und ihrer Inhaber (Rufzeichenliste)"](https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Frequenzen/SpezielleAnwendungen/Amateurfunk/faq_table.html#FAQ648458)

* Download standalone apache java program "pdfbox"

[pdfbox homepage](https://pdfbox.apache.org), [Download directory](https://pdfbox.apache.org/download.html)

Under "Command line tools", "PDFBox standalone", download jar file.
e.g. [PDFBox v3.0.2 (stable)](https://www.apache.org/dyn/closer.lua/pdfbox/3.0.2/pdfbox-app-3.0.2.jar)

* Extract raw text from PDF file

Usage: java -jar pdfbox-app-3.0.2.jar export:text --input=<input.pdf> --output=<output.txt>

* Extract operator data (call sign, operator class, name, address)

Call ./rufz-extract-from-txt.py <raw-text-file> > <operator-csv-file>

* Geocode all addresses and write them to a CSV file

Ugly, i know: change txt file name in file "rufz-geocode.py" (around line 82):

=> file = open(\<path <operator-csv-file>\>)

and then start "rufz-geocode.py"

Output is written to CSV file "rufzeichen-geocoded.csv". It includes
comma-separated values of longitude, latitude, call sign, amateur
radio class, name of operator, and address (semicolon separated
parts). (obsolete: If there are multiple addresses for an operator, there is one
line for each address)

"Nominatim" is the name of openstreetmaps locator service. Cause it allows
max. one request per second, conversion needs at least 60000 seconds, so
roughly 17 hours.

If the geocoding program crashes for some reason - e.g. locator not
available on three retries, network connection down - on the next
start the program resumes geocoding beginning at the last position, so
that not all work done so far is lost. The program can also be
interrupted gracefully by keyboard ctrl-c (SIGINT).

The file "rufzeichen-seen.txt" contains always the last seen operator
by the program. You must delete it after complete conversion to start
a new conversion, and also the file "rufzeichen-geocoded.txt", cause
the file will always be appended.

* Import data

in e.g. Google Earth by direct import (see under file menu) or import
as CSV delimited data into a GIS program - QGis is GREAT. The layer
can be exported a KML file, which can be imported into Google Earth or
Google Maps.
