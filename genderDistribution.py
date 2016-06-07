# Script calculates the percent of authors in a database with male, female, unisex, or unassigned names. Will count multiple authors once; accuracy of gender assignment has been validated by a (not-particuarly random) set of 100 names. cu

#system functions
from __future__ import division
import os
import sys
from datetime import datetime #system date
import csv
import argparse
from collections import Counter

#gendering
from genderComputer.genderComputer import GenderComputer
#parsing
import bibtexparser as b #module for bibtex parsing, obviously
from bibtexparser.bparser import BibTexParser #add customization
from bibtexparser.customization import *

#plot stuff; transitioning to seaborn asap
import numpy as np
import seaborn




def startUp(bib):
    today = datetime.today()
    #gc = GenderComputer(os.path.abspath('genderComputer/nameLists')) #make gendercomputer
    bib = bib
    records = parseFile(bib)
    data = getDBCounts(records)
    return data

def customizations(record):
    """Use some functions delivered by the library
    :param record: a record
    :returns: -- customized record
    """
    record = type(record)
    record = doi(record)
    record = convert_to_unicode(record)
    record = author(record)
    return record

def parseFile(bib_file):
    """parse the bib file

    :param bib_file: bibtex file to be parsed
    :returns: -- a bibtex file object
    """
    with open(bib_file) as bibtex_file:
        parser = BibTexParser() #import the parsers
        parser.homogenize = True
        parser.customization = customizations #add some customizations defined earlier
        data = b.load(bibtex_file, parser = parser) #process data yah!
        return data

def clean_tex(s): #tex files are super gross; lil hacky though + might be losing data
    badSubstrings = ["{","}"]
    for badSubstring in badSubstrings:
        s = s.replace(badSubstring, "")
    return s

### the workhorse ###

def getDBCounts(data):
    #set variables to count all the things with a Counter object!
    c = Counter({"authorCount":0,
                "unisex":0,
                "women":0,
                "men":0,
                "unavailable":0,
                "no_author":[],
                "no_title":[],
                "no_gender":[]
                })

    gc = GenderComputer(os.path.abspath('genderComputer/nameLists')) #make gendercomputer for defining names

    def _countGenders(authors, c, gc=gc): #defining an inner function cause it's faster to call this way
        for author in authors:
            gender = gc.resolveGender(clean_tex(author), None) #TODO: feed affiliation in as a starting place to look for name assignment
            if gender == 'male': c["men"] += 1
            elif gender == 'female': c["women"] += 1
            elif gender == 'unisex': c ["unisex"] +=1
            else:
                c["unavailable"] += 1
                c["no_gender"].append(author)

    def _countJournals(entry = ""):
        return        #add in Joel's fn to count journals w. regexs; or use other tactics?
        #needs a c["journals"] field? doesn't retain journal - gender link, as currently conceptualized
        #not sure how to use this info; BUT probably when it has a "check if OA" option it'll need to be its own function

    ##############################
    ### the actual processing ###

    for entry in data.entries: #for each paper processed
        #get titles + author lists sorted out
        title = clean_tex(entry["title"]) if "title" in entry else c["no_title"].append(entry)

        if "author" in entry:
            authors = entry["author"]
            c["authorCount"] = c["authorCount"] + len(authors)
        else: c["no_author"].append(title)

        _countGenders(authors, c)
        _countJournals(c)
        #append the length of the author list to the author count



    return c #return all the data in a counter format! it's a pain to work with I think;; or at least seaborn doesn't like it much :(


if __name__ == '__main__':
    d = startUp(sys.argv[1])
    print "\ntotal authors found: {}".format(d['authorCount'])
    print "assigned men: {}".format(d['men'])
    print "assigned women: {}".format(d['women'])
    print "assigned unisex: {}".format(d['unisex'])
    print "unassigned: {}".format(d['unavailable'])


# """
# TODO: more maintained gender calculator?
# TODO: turn hacky stats into a function; decide if I want this to be a script or more interactive
#
# ##########################
# ###Old Stuff###
#
# for key in stats:
#     value = stats[key]
#     percent = value/auCount*100 #probably should fix so it can't break if dividing by zero
#     percents[key] = percent
#
#
# print stats
# print percents
# print auCount
#
# plt.bar(range(len(stats)), percents.values(), align='center', color="#2aa198")
# plt.xticks(range(len(percents)), percents.keys(), color="#657b83")
# plt.xlabel('Genders' + '\n' +  '(plot generated ' + 'May 14 2015' +')', color="#073642")
# plt.ylabel('"""', color="#073642")
#
#
# #plt.show()
# """"
