#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II FS 17, Übung 2
# Übung 4, Aufgabe 1
# Author: Patrick Haller

import lxml.etree as ET
import glob
import operator


def main():
    """Get frequencies for XML file in directory "SAC"
    (change path if necessary)
    """
    getfreqwords('SAC', 'outfile.txt')


def extract(file):
    """Get lemmatized sentences 
    comment line 30 if you want to include sentences
    in captions.
    """
    context = ET.iterparse(file, events=("start", "end"))
    context = iter(context)
    event, root = next(context)
    for event, elem in context:
        # find sentences, ignore picture captions
        if ((event == "end") and 
                (elem.tag == 's') and 
                (elem.getparent().tag != 'caption')):
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
    def check_frequency(sentence, n):
        """get n most frequent sentences
        """
        sentence_hash = hash(sentence)
        #store hashes in dictionary
        if hash(sentence) in hash_frequencies:
            hash_frequencies[sentence_hash] += 1
        else:
            hash_frequencies[sentence_hash] = 1
        #fill list with n most frequent elements
        if ((len(most_frequent) < n) and 
                (sentence not in [item for item,_ in most_frequent])):
            most_frequent.append((sentence, hash_frequencies[sentence_hash]))
        else:
            #if sentence already among n most frequent, update count
            if sentence in [item for item,_ in most_frequent]:
                i = most_frequent.index(
                    (sentence, hash_frequencies[sentence_hash]-1))
                most_frequent[i] = (sentence, hash_frequencies[sentence_hash])
                most_frequent.sort(reverse=True,key=lambda tup: tup[1])
            #if sentence not among n most frequent but more frequent than
            #least frequent in list, replace them,
            else:
                if hash_frequencies[sentence_hash] >= most_frequent[-1][1]:
                    most_frequent[-1] = (sentence, hash_frequencies[sentence_hash])
                    most_frequent.sort(reverse=True,key=lambda tup: tup[1])

    hash_frequencies = {}
    most_frequent = []
    files = [file for file in glob.glob(
        '{}/{}'.format(indir, 'SAC-Jahrbuch*_mul.xml')
        )]
    try:
        for file in files:
            for entry in extract(file):
                if len(entry.split()) >= 6:
                    check_frequency(entry, 20)
    finally:
        outfile = open(outfile, 'w')
        for k,v in most_frequent:
            outfile.write('{} \t {} \n'.format(v,k))
        outfile.close()

if __name__ == '__main__':
        main()