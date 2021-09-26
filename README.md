# German-Amateur-Radio-Operator-Locations

Convert adresses of amateur radio operators from the Bundesnetzagentur to geocoded file with latitude/longitude
=====================

<<<<<<< HEAD
Requirements: java jre, python3, python module geopy

=> pip3 install geopy

Tested on Ubuntu 18.04 LTS.

The project is inspired by
[CallmapGermany](https://github.com/df8oe/CallmapGermany) from Ulrich
Thiel.

=======
Requirements: java jre, python3

Tested on Ubuntu 18.04 LTS.

>>>>>>> a15925a27b81f8bea1e0beb51ff357d04a6bff2a
* Download PDF with adresses of amateur radio operators from the Bundesnetzagentur

["Verzeichnis der zugeteilten deutschen Amateurfunkrufzeichen und ihrer Inhaber (Rufzeichenliste)"](https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Frequenzen/Amateurfunk/Rufzeichenliste/Rufzeichenliste_AFU.html)

* Download standalone apache java program "pdfbox"

[pdfbox homepage](https://pdfbox.apache.org), [Download directory](https://pdfbox.apache.org/download.html)

Under "Command line tools", "PDFBox standalone":
e.g. [PDFBox v2.0.24 (stable)](https://www.apache.org/dyn/closer.lua/pdfbox/2.0.24/pdfbox-app-2.0.24.jar)

* Extract text from pdf

Usage: java - jar pdfbox.jar ExtractText <input.pdf> <output.txt>

* Geocode all addresses and write them to a csv

Ugly, i know: change file name in file "geocode2.py" (around line 50):

=> file = open(<name of text file here)

and then start "geocode.py"

"Nominatim" is the name of openstreetmaps locator service. Cause it allows
max. one request per second, conversion needs ca. 77000 seconds, so
roughly 22 hours.

If the program crashes for some reason - e.g. locator not available on
three retries, network connection down - on the next start the program
resumes geocoding beginning at the last position, so that not all work
done so far is lost.

<<<<<<< HEAD
* Import data

in e.g. Google Earth by direct import (see under file menu) or import
as csv delimited data into a GIS program - QGis is GREAT. The layer
can be exported a KML file, which can be imported into Google Earth or
Google Maps.
=======
Geocoded data for 2021-08-02 are checked in.

* Import data in e.g. Google Earth

- direct import

OR

- import as delimited data into a QGis (great GIS program) layer, and
  export that layer to a KML file, which can be imported in Google
  Earth.
>>>>>>> a15925a27b81f8bea1e0beb51ff357d04a6bff2a
