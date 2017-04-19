#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PCL II FS 17, Übung 2
# Übung 4, Aufgabe 2
# Author: Patrick Haller

import lxml.etree as ET
import bz2
import urllib.request
import random


def main():
    path = urllib.request.urlopen('https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2')
    infile = bz2.BZ2File(path)
    gettitles(infile, 'testfile.txt', 'trainfile.txt', 100)


def gettitles(infile, testfile, trainfile, k):
    """Extract all article titles from infile, 
    write k thereof to testfile, rest to trainfile
    """
    test_list = []
    t = 0
    m = 0
    train_out = open(trainfile, 'w')
    context = ET.iterparse(infile, events=("start", "end"))
    # Iterate over all elements in the subtree in document order (depth first pre-order), starting with this element.
    context = iter(context)
    event, root = next(context)
    try:
        for event, elem in context:
            # find titles
            if event == "end" and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
                title = elem.text
                # Algorithm R
                if t < k:
                    test_list.append(title)
                else:
                    m = random.randint(e0, t)
                    if m < k:
                        train_out.write('%s\n' % test_list[m])
                        test_list[m] = title
                    else:
                        train_out.write('%s\n' % title)     
                root.clear()
                elem.clear()
                t += 1
        del context
        train_out.close()
    finally:
        with open(testfile, 'w') as test_out:
            for title in test_list:
                test_out.write('%s\n' % title)

if __name__ == '__main__':
        main()