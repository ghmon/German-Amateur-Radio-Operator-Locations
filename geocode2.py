#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import logging

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

# Usage policy Nominatim
# <https://operations.osmfoundation.org/policies/nominatim>
# maximum of 1 request per second
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

# numSeenRecords: all records including those who where skipped
if os.path.isfile("rufzeichen-seen.txt"):
    records_seen = open( "rufzeichen-seen.txt", "r+" )
else:
    records_seen = open( "rufzeichen-seen.txt", "w+" )
    records_seen.write( "0" )

records_seen.seek(0, 0)
numSeenRecords = int(records_seen.read())

logger.debug( "#SR: seen records: " + str(numSeenRecords) )

rufzeichen = open( "rufzeichen.csv", "a+")
if numSeenRecords == 0:
    rufzeichen.write( 'lon, lat, callsign, class, name, address' + '\n' )

file = open('2021-08-02-Amateurfunk-Funkamateure-Rufzeichenliste_AFU-CallSigns-Bundesnetzagentur.txt', 'r')

# Parentized part in split expression record in splitted records
callsigns = re.compile( r'(D[A-Z0-9]+),' )

# remove all empty lines and "Seite xxx"
lines = re.split( r'\n', file.read() )

data = ""
for line in lines:
    if not re.match( r" +$|^Seite", line ):
        data = data + line

# split on callsigns
callsigns_alldata = re.split( callsigns, data )

it = iter( callsigns_alldata )
next(it) # skip empty entry (?)

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
        numSeenRecords = numSeenRecords + 1
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

        retry = 3
        
        while retry > 0:

            try:
                location = locator.geocode( address, timeout=10 )
                
                if location:
                    record = "{}, {}, {}, {}, {}, {}\n".\
                        format( location.longitude,
                                location.latitude,
                                callsign, csclass, csname, address.strip() )
                    rufzeichen.write( record )
                    logger.debug( "#CSV-Written: " + record )
                    # logger.debug( "#Locator-Address: " + str(location.address) )
                    # logger.debug( "#Locator-Raw: " +str(location.raw) )

                retry = 0
                
            except GeocoderTimedOut as e:
                print("Error: geocoder timeout: " + e.message)
                retry = retry - 1

            except GeocoderServiceError as e:
                print("Error: geocoder service error: " + e.message)
                retry = retry - 1

            except GeocoderUnavailable as e:
                print("Error: geocoder unavailable: " + e.message)
                retry = retry - 1

        time.sleep(1)

    numSeenRecords = numSeenRecords + 1
    numProcessedRecords = numProcessedRecords + 1

    records_seen.seek( 0, 0 )
    records_seen.write( str(numSeenRecords) )
    records_seen.flush()

    rufzeichen.flush()

    print( "# seen: " + str(numSeenRecords) )
    print( "# processed: " + str(numProcessedRecords) )
