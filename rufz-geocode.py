#!/usr/bin/env python3

import os
import re
import time
import logging

# Usage policy Nominatim: maximum of 1 request per second. Results
# must be cached on your side. Clients sending repeatedly the same
# query may be classified as faulty and blocked.
# <https://operations.osmfoundation.org/policies/nominatim>
from geopy.geocoders import Nominatim
# need API-Keys: TomTom, Bing, Baidu, GeocodeEarth, GoogleV3

from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError
from geopy.exc import GeocoderUnavailable

# ctrl-c: graceful exit
import signal
STOP_PROGRAM = False
def sigint_handler(signum, frame):
    global STOP_PROGRAM
    STOP_PROGRAM = True
    print("ctrl-c, graceful exit...")

signal.signal(signal.SIGINT, sigint_handler)

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
# is terminated otherwise, you have not to geocode all addresses
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

# !!! including all skipped records
numSeenRecords = int(records_seen.read())

logger.debug( "#SR: seen records: " + str(numSeenRecords) )

#
# Create output file
#

rufzeichen = open( "rufzeichen-geocoded.csv", "a+")
if numSeenRecords == 0:
    rufzeichen.write( 'lon, lat, callsign, class, name, address' + '\n' )

#
# Read and preprocess input file
#

records = []
with open('2024-05-01-Amateurfunk-Funkamateure-Rufzeichenliste_AFU-CallSigns-Bundesnetzagentur.csv', 'r') as f:
    records = f.read().splitlines()

locator = Nominatim( user_agent="geocode radio amateur addresses" )

numProcessedRecords=0

# Start from last position when exited (crash recovery)
for num in range(numSeenRecords+1, len(records)):

    # callsign,class,name,addr1,addr2
    recs = records[num].split(",")
    
    logger.debug( "#CS: " + recs[0] )

    print(recs)
    if recs[3] == "n/a" and recs[4] == "n/a":
        logger.debug( f"skip record {num}" )
        # skip record, no addresses
        numSeenRecords += 1
        records_seen.seek( 0, 0 )
        records_seen.write( str(numSeenRecords) )
        records_seen.flush()
        continue

    # split anew addresses only cause ";" separated also class + name
    # from addresses.
    address = recs[4] if recs[4] else recs[3]

    retries = 3
    while retries > 0:
        try:
            location = locator.geocode( address, timeout=10 )

            if location:
                record = "{}, {}, {}, {}, {}, {}\n".format(
                    location.longitude, location.latitude,
                    recs[0], recs[1], recs[2], address )
                rufzeichen.write( record )
                logger.debug( "#CSV-Written: " + record )

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
    # print( "# processed: " + str(numProcessedRecords) )

    if STOP_PROGRAM:
        print("Exiting...")
        exit(0)
