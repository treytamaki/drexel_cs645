#!/usr/bin/python

import base64
import binascii
import logging
from itertools import izip
import sys
import struct
import argparse
import string

logging.basicConfig(
    format = "%(levelname)-5s %(module)s.py: line %(lineno)d: %(message)s",
    level  = logging.DEBUG
)

ONE = 'ct1.hex'
TWO = 'ct2.hex'
THREE = 'ct3.hex'
FOUR = 'ct4.hex'
FIVE = 'ct5.hex'
SIX = 'ct6.hex'

log = logging.getLogger('xor')

files = list()

testMode = False

if(testMode) :
    files = ["testTxt1","testTxt2"]
else :
    files = [ONE, TWO, THREE, FOUR, FIVE, SIX]

def cipher2list(cipher_file_name):
    '''Load in the cipher text and return a list of ASCII encoded hex bytes
    >>> print cipher2list('ct1.hex')[1:10]
    ['0x6b', '0x6d', '0x34', '0x38', '0x63', '0x47', '0x4b', '0x58', '0x1f']
    '''
    with open(cipher_file_name) as f:
        return f.read().split()

def make_cipher_dict(list_of_files):
    '''Give a list of files, return a dict whose key is the filename and
    whose value is a list of ASCII encoded bytes
    >>> print make_cipher_dict(['ct1.hex'])['ct1.hex'][0:9]
    ['0x17', '0x6b', '0x6d', '0x34', '0x38', '0x63', '0x47', '0x4b', '0x58']
    '''
    ciphers = {}
    for l in list_of_files:
        ciphers[l] = cipher2list(l)

    return ciphers

ciphertexts = make_cipher_dict(files)

# Example xor
outAsHex = False
outAsAscii = False

# Tracks the names of the ciphertexts that were xored togethed
xorOutputFileNames = []

# Trackes the decode attempts
decodeAttemptFileNames = []

def xor_ascii_hex(x,y):
    '''XOR two ASCII encoded hex bytes and return the hex encoded value.
    >>> xor_ascii_hex('0x68', '0x19')
    '0x71'
    '''
    return hex(int(x, 16) ^ int(y, 16))

def xor_hex_char(hex_x, chr_y):
    '''XOR hex encoded ascii with a char.
    >>> xor_hex_char('0x61', ' ')
    '0x41'
    '''
    return xor_ascii_hex(hex_x, hex(ord(chr_y)))

def byte2char(b):
    '''Utility to turn a hex encoded byte into a char
    >>> print byte2char('0x61')
    a
    '''
    return chr(int(b, 16))

def xor_lists(x,y):
    '''XOR two lists of hex encoded values and return the result.  Must be
    the same length (which they are for this project: 128 )
    >>> xor_lists(['0x00', '0x01', '0x00', '0x01'], ['0x00', '0x00', '0x01', '0x01'])
    ['0x0', '0x1', '0x1', '0x0']
    '''
    return [xor_ascii_hex(a,b) for a,b in zip(x,y)]

def hex2char(hex_list):
    '''Convert hex encoded to characters (some may not be printable)
    >>> hex2char(cipher2list('ct1.hex'))[1:9]
    ['k', 'm', '4', '8', 'c', 'G', 'K', 'X']
    '''
    return [chr(int(x, 16)) for x in hex_list]

def filter_non_printable(hex_string):
    return [x for x in hex_string if x in string.printable]

def slice_by(number):

    def slice_number(lst):
        return [lst[x:x+number] for x in range(0, len(lst), number)]

    return slice_number

if __name__=="__main__":
    import doctest
    doctest.testmod()

    parser = argparse.ArgumentParser(description='Xor cracker')
    parser.add_argument('cribText', help='The crib text')
    parser.add_argument('findText', help='The text to find')

    args = parser.parse_args()

    cipherDict = make_cipher_dict(files)

    for key1 in cipherDict :
        for key2 in cipherDict :
            if(key1 != key2) :
                log.debug("Test with: "+key1+"and "+key2)
                log.debug((hex2char(xor_lists(cipherDict[key1],cipherDict[key2]))))
