#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II FS 17, Übung 2
# Übung 4, Aufgabe 1
# Author: Patrick Haller

import lxml.etree as ET
import glob
import operator


def main():
        getfreqwords('SAC', 'ouftfile_improved.txt')


def extract(file):
    """Get lemmatized sentences 
    """
    context = ET.iterparse(file, events=("start", "end"))
    context = iter(context)
    event, root = next(context)
    for event, elem in context:
        # find sentences, ignore picture captions
        if event == "end" and elem.tag == 's' and elem.getparent().tag != 'caption':
            sent = ''
            for word in elem.iterfind('.//w'):
                # check if attribute exists
                if 'lemma' in word.attrib:
                    sent = '{} {}'.format(sent,word.attrib['lemma'])
            yield sent
            elem.clear()
            root.clear()

def getfreqwords(indir, outfile):
    """Get 20 most frequent lemmatized sentences
    from a collection of xml files (indir) and write
    them to a textfile (outfile)
    """
    lemma_dict = {}
    files = [file for file in glob.glob(
        '{}/{}'.format(indir, 'SAC-Jahrbuch*_mul.xml')
        )]
    try:
        for file in files:
            for entry in extract(file):
                if len(entry.split()) >= 6:
                    if entry in lemma_dict:
                        lemma_dict[entry] += 1
                    else:
                        lemma_dict[entry] = 1
    finally:
        lemma_dict_sorted = sorted(
            lemma_dict.items(), key=operator.itemgetter(1), reverse=True
            )
        outfile = open(outfile, 'w')
        for k,v in lemma_dict_sorted[0:20]:
            outfile.write('{} \t {} \n'.format(v,k))
        outfile.close()

if __name__ == '__main__':
        main()