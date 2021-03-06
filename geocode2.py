#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Imports
#

import os
import re
import time
import logging

# Usage policy Nominatim: maximum of 1 request per second
# <https://operations.osmfoundation.org/policies/nominatim>
from geopy.geocoders import Nominatim

from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError
from geopy.exc import GeocoderUnavailable

# - all following locators need API keys
# from geopy.geocoders import TomTom
# from geopy.geocoders import Bing
# from geopy.geocoders import Baidu
# from geopy.geocoders import GeocodeEarth
# from geopy.geocoders import GoogleV3

#
# Setup logging
#

logger = logging.getLogger('Debug logger')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
# create formatter
formatter = logging.Formatter( '%(levelname)s - %(message)s' )
#    '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
# add formatter to ch
ch.setFormatter(formatter)
logger.addHandler(ch)

#
# Setup crash recovery
#

# Read number of *seen* records on last exit. If the program crashes or
# is terminated otherwise you have not to geocode all addresses
# again. If you want to start from the beginning delete file
# "rufzeichen-seen.txt".

# numSeenRecords: all records including those who where skipped cause
# no addresses given.
if os.path.isfile("rufzeichen-seen.txt"):
    records_seen = open( "rufzeichen-seen.txt", "r+" )
else:
    records_seen = open( "rufzeichen-seen.txt", "w+" )
    records_seen.write( "0" )

records_seen.seek(0, 0)
numSeenRecords = int(records_seen.read())

logger.debug( "#SR: seen records: " + str(numSeenRecords) )

#
# Create output file
#

rufzeichen = open( "rufzeichen.csv", "a+")
if numSeenRecords == 0:
    rufzeichen.write( 'lon, lat, callsign, class, name, address' + '\n' )

#
# Read and preprocess input file
#

file = open('2021-08-02-Amateurfunk-Funkamateure-Rufzeichenliste_AFU-CallSigns-Bundesnetzagentur.txt', 'r')
lines = re.split( r'\n', file.read() )
file.close()

data = ""
for line in lines:
    # remove all empty lines and "Seite xxx"
    if not re.match( r" +$|^Seite", line ):
        data = data + line

# Parentized part in split expression is in splitted records
callsigns = re.compile( r'(D[A-Z0-9]+),' )
# split on callsigns
callsigns_alldata = re.split( callsigns, data )

it = iter( callsigns_alldata )
next(it) # skip empty entry (?)

#
# Start work from last position when exited
# (crash recovery)
#

# skip already processed numSeenRecords records
for i in range(2*(numSeenRecords+1)):
    next(it)

locator = Nominatim( user_agent="geocode radio amateur addresses" )

numProcessedRecords=0

for callsign in it:

    logger.debug( "#CS: " + callsign )

    personal_data = next(it)

    if not re.search( r";", personal_data ):
        # skip record, no addresses
        numSeenRecords += 1
        records_seen.seek( 0, 0 )
        records_seen.write( str(numSeenRecords) )
        records_seen.flush()
        continue

    # personal_data: "class,name; address,?[address,]{0,}"
    personal_data = re.split( r";", personal_data )
    # now: [class+name, adress1, address2, ...]

    clsname = re.split( r",", personal_data[0] )
    csclass = clsname[0].strip()
    csname  = clsname[1].strip()

    logger.debug( "#CL: " + csclass )
    logger.debug( "#NA: " + csname )

    # split anew addresses only cause ";" separated also class + name
    # from addresses.
    addresses = re.split( ",", ";".join(personal_data[1:]) )
    logger.debug( "#ADR_ALL: " + "".join( addresses ) )

    for address in addresses:

        retries = 3
        
        while retries > 0:

            try:
                location = locator.geocode( address, timeout=10 )
                
                if location:
                    record = "{}, {}, {}, {}, {}, {}\n".\
                        format( location.longitude,
                                location.latitude,
                                callsign, csclass, csname, address.strip() )
                    rufzeichen.write( record )
                    logger.debug( "#CSV-Written: " + record )
                    # location.address, location.raw

                retries = 0
                
            except ( GeocoderTimedOut,
                     GeocoderUnavailable,
                     GeocoderServiceError ) as e:
                print( "Error: " + str(e) )
                retries = retries - 1

        # Usage policy Nominatim: maximum of 1 request per second
        time.sleep(1)

    numSeenRecords += 1
    numProcessedRecords += 1

    records_seen.seek( 0, 0 )
    records_seen.write( str(numSeenRecords) )
    records_seen.flush()

    rufzeichen.flush()

    print( "# seen: " + str(numSeenRecords) )
    print( "# processed: " + str(numProcessedRecords) )
