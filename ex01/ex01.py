#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II FS 17, Übung 2
# Übung 4, Aufgabe 1
# Author: Patrick Haller

import lxml.etree as ET
import glob
import operator


def main():
    try:
        getfreqwords('SAC', 'ouftile.txt')
    except MemoryError:
        print('Too much memory used. Optimize your program.')


def extract(file):
    """Get lemmatized sentences 
    """
    for _, sentence in ET.iterparse(file, tag='s'):
        # ignore sentences in picture captions
        if sentence.getparent().tag != 'caption':
            sent = ''
            for word in sentence.iterfind('.//w'):
                # check if attribute exists
                if 'lemma' in word.attrib:
                    sent = '{} {}'.format(sent,word.attrib['lemma'])
                word.clear()
            yield sent
        sentence.clear()

def getfreqwords(indir, outfile):
    """Get 20 most frequent lemmatized sentences
    from a collection of xml files (indir) and write
    them to a textfile (outfile)
    """
    lemma_dict = {}
    files = [file for file in glob.glob(
        '{}/{}'.format(indir, 'SAC-Jahrbuch*_mul.xml')
        )]
    for file in files:
        for entry in extract(file):
            if len(entry.split()) >= 6:
                if entry in lemma_dict:
                    lemma_dict[entry] += 1
                else:
                    lemma_dict[entry] = 1
    lemma_dict_sorted = sorted(
        lemma_dict.items(), key=operator.itemgetter(1), reverse=True
        )
    outfile = open(outfile, 'w')
    for k,v in lemma_dict_sorted[0:20]:
        outfile.write('{} \t {} \n'.format(v,k))
    outfile.close()


if __name__ == '__main__':
        main()