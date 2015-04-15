# coding: utf-8

# In[1]:

from __future__ import division

"""bibtex parsing"""
import os
import bibtexparser as b #module for bibtexin'
from bibtexparser.bparser import BibTexParser #import to add customization
from bibtexparser.customization import *

"""journal name comparison"""
from difflib import SequenceMatcher
import re # regular expression searching

"""plotting functions"""
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

"""date time functions """
from datetime import datetime #idk bring in the system date or whatever

"""csv"""
import csv


# In[2]:

today = datetime.today()
bib = 'CriticalOpenNeuro.bib' #bring that bib file in


# In[3]:

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


# In[4]:

def parseFile(bib_file):
    """parse the bib file
    
    :param bib_file: bibtex file to be parsed
    :returns: -- a bibtex file object
    """
    with open(bib_file) as bibtex_file: 
        parser = BibTexParser()
        parser.homogenize = True        
        parser.customization = customizations
        data = b.load(bibtex_file, parser = parser)
        return data



data = parseFile(bib) #run the parse file
articles = []

for entry in data.entries: # get just article entries
    if entry["type"] == u'article':
        articles.append(entry)

journalTally = {}

for entry in articles:
    try: # some of your articles have no journal entry
        journal = entry[u'journal']
        if re.search("PLOS", journal.upper()) != None: # regex search in caps for the journal dupe text
            journal = "PLoS" # if you find it, replace journal with that
        if re.search("NATURE", journal.upper()) != None:
            journal = "Nature"
    except: 
        journal = "???"
        print "an entry was missing the journal key"
    
    try:
        journalTally[journal] += 1 # if the key exists, increment by 1
    except:
        journalTally[journal] = 1 # if it doesn't, create it

print journalTally

def similar(a, b): # this will tell give you a % for how similar one string is to the other. could be useful for more intelligent matching
    return SequenceMatcher(None, a, b).ratio()


# for key in stats:
#     value = stats[key]
#     percent = value/auCount*100 #probably should fix so it can't break if dividing by zero
#     percents[key] = percent


# # In[11]:

# print stats
# print percents
# print auCount


# plt.bar(range(len(stats)), percents.values(), align='center', color="#2aa198")
# plt.xticks(range(len(percents)), percents.keys(), color="#657b83")
# plt.xlabel('Gender Assigned (generated ' + str(today) +')', color="#073642")
# plt.ylabel('Percents', color="#073642")

