#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II FS 17, Übung 2
# Übung 4, Aufgabe 1
# Author: Patrick Haller

import lxml.etree as ET
import glob
import operator

def main():
    mydict = {}
    files = [file for file in glob.glob('SAC/SAC-Jahrbuch*_mul.xml')]
    #print(files)
    for file in files:
        for entry in extract(file):
            if len(entry.split()) >= 6:
                if entry in mydict:
                    mydict[entry] += 1
                else:
                    mydict[entry] = 1
    sorted_x = sorted(mydict.items(), key=operator.itemgetter(1), reverse=True)
    outfile = open('outfile.txt', 'w')
    for k,v in sorted_x:
        outfile.write('{} \t {} \n'.format(v,k))
    outfile.close()


def extract(file):
    '''Get lemma sentences 
    '''
    for _, sentence in ET.iterparse(file, tag='s'):
        sent = ''
        for word in sentence.iterfind('.//w'):
            # check if attribute exists
            if 'lemma' in word.attrib:
                sent = '{} {}'.format(sent,word.attrib['lemma'])
        yield sent
        sentence.clear()

def getfreqwords(indir, outfile):
    pass
    # indir = Verzeichnis mit XML-Daten
    # outfile = Textdatei für Ausgabe
    # durch alle XML-Dateien vom Schema ’SAC-Jahrbuch_XXXX_mul.xml’ durchgehen


if __name__ == '__main__':
        main()