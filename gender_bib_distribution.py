ls

# coding: utf-8

# In[1]:

from __future__ import division

"""gendering"""
from genderComputer.genderComputer import GenderComputer

"""bibtex parsing"""
import os
import bibtexparser as b #module for bibtexin'
from bibtexparser.bparser import BibTexParser #import to add customization
from bibtexparser.customization import *

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
gc = GenderComputer(os.path.abspath('genderComputer/nameLists')) #make gendercomputer


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


# In[5]:

women = 0
men = 0
uni = 0
notav = 0
auCount = 0

unavailable = []


# In[6]:



def countGender(ts=True):
    """take the bib database and count genders of authors
    """ 
    global auCount
    global notav
    global uni
    global men
    global women
    global unavailable
    for entry in data.entries:
        title = entry["title"]
        if "author" in entry:
            authors = entry["author"] 
        elif ts==True:
            print "no author in", title
        for j in authors:
            auCount += 1
            gender = gc.resolveGender(j, None) #resolve gender, yay
            if gender == 'male':
                men += 1
            elif gender == 'female':
                women += 1
            elif gender == 'unisex':
                uni += 1
            else:
                notav += 1 
                if ts == True:
                    print j, title


# In[7]:

data = parseFile(bib) #run the parse file
countGender(False)


# In[8]:

"""writing names unassigned to a file for troubleshooting"""
with open('unavailable_gender', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(unavailable)


# In[9]:

stats = {'Women':women, 'Men':men, 'Unisex':uni, 'Not Available':notav}
percents = {'Women':women, 'Men':men, 'Unisex':uni, 'Not Available':notav}


# In[10]:

for key in stats:
    value = stats[key]
    percent = value/auCount*100 #probably should fix so it can't break if dividing by zero
    percents[key] = percent


# In[11]:

print stats
print percents
print auCount


# In[20]:

plt.bar(range(len(stats)), percents.values(), align='center', color="#2aa198")
plt.xticks(range(len(percents)), percents.keys(), color="#657b83")
plt.xlabel('Gender Assigned (generated ' + str(today) +')', color="#073642")
plt.ylabel('Percents', color="#073642")


# In[21]:

plt.savefig('gender_distr.png', bbox_inches='tight',transparent=True)


# In[ ]:



