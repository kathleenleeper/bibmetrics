# Script calculates the percent of authors in a database with male, female, unisex, or unassigned names. Will count multiple authors once; accuracy of gender assignment has been validated by a (not-particuarly random) set of 100 names. cu

from __future__ import division

"""gendering"""
from genderComputer.genderComputer import GenderComputer 

"""bibtex parsing"""
import os
import bibtexparser as b #module for bibtex parsing, obviously
from bibtexparser.bparser import BibTexParser #add customization
from bibtexparser.customization import *

"""plotting functions"""
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

"""date time functions """
from datetime import datetime #system date

"""csv"""
import csv


# In[2]:

today = datetime.today()
gc = GenderComputer(os.path.abspath('genderComputer/nameLists')) #make gendercomputer


# In[3]:

bib = 'CriticalOpenNeuro.bib' #bibtex file of choice; should modify for user-defined bib

# In[4]:

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


# In[5]:

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
    
def clean_tex(s): #tex files are super gross
    badSubstrings = ["{","}"]
    for badSubstring in badSubstrings:
        s = s.replace(badSubstring, "")
    return s

# In[6]:

"""set variables"""

auCount = 0
notav = 0
uni = 0
men = 0
women = 0
unavailable = []

# In[7]:

def countGender(ts=True): #ts stands for troubleshooting, for papers w/ no authors or weird titles -- eventually build a feature that presents unassigned names and asks for manual assignment and modifies a database accordingly
    """take the bib database and count authors
    """ 
    global auCount
    global notav 
    global uni 
    global men 
    global women 
    global unavailable 
    no_author = []
    no_title = []
    no_gender = []
    for entry in data.entries:
        if "title" in entry:
            title = clean_tex(entry["title"])
        else:
            no_title.append(entry)
        if "author" in entry:
            authors = entry["author"] 
        else:
            no_author.append(title)
        for j in authors:
            j = clean_tex(j)
            auCount += 1
            gender = gc.resolveGender(j, None) #resolve gender, yay -- assumes all names are American though;
            if gender == 'male':
                men += 1
            elif gender == 'female':
                women += 1
            elif gender == 'unisex':
                uni += 1
            else:
                notav += 1 
                no_gender.append(j)
    if ts==True:
        print "No author found in these Papers:\n\n" + '\n'.join(no_author)
        print "\nNo gender on these Names:\n" + '\n'.join(no_gender) #eventually so I can manually add a list of names that I know, but the social security database doesn't
        print "\n\nNo title on these entries:\n\n" + '\n'.join(no_title)  
  


# In[8]:

data = parseFile(bib) #r
countGender(ts=True)


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


# In[12]:

plt.bar(range(len(stats)), percents.values(), align='center', color="#2aa198")
plt.xticks(range(len(percents)), percents.keys(), color="#657b83")
plt.xlabel('Genders' + '\n' +  '(plot generated ' + 'May 14 2015' +')', color="#073642")
plt.ylabel('% of bibliography', color="#073642")


plt.show()




