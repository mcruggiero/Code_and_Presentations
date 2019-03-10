
#The goal of this project is to download all of the 2018 SAT information and append all of that information
#into a preexisting data-frame

import os
import pandas as pd
import numpy as np

os.listdir()

#This is the starter file which has some of the 2017 SAT information
merged = pd.read_csv("./combined_2017.csv")

import requests

#All of the SAT urls follow the format /pdf/2018-*state*-sat-suite-assessments-annual-report.pdf
#So lets download the buggers DC will probably be a pain, so we can fix that too

states = [x.replace(" ", "-") if x != 'district of columbia' else "district-columbia" for x in list(merged["State"].str.lower())]

for state in states:
    url = "https://reports.collegeboard.org/pdf/2018-{}-sat-suite-assessments-annual-report.pdf".format(state)
    r = requests.get(url, allow_redirects=True)
    open('2018_SAT_{}_Data.pdf'.format(state), 'wb').write(r.content)

#Just a little check to see if all of the files downloaded correctly.

count = 0
for file in os.listdir():
    if file[-3:] == "pdf":
        print(count,file)
        count += 1

import slate3k as slate

def pdf_view(file):
    mine  = []
    with open(file, 'rb') as f:
        doc = slate.PDF(f)

    pdf_miner =  [x for x in doc[3].split("\n") if x != ""]
    for i in range(len(pdf_miner)):
        mine.append(pdf_miner[i].lstrip())

    return(mine)

pdf_view("2018_SAT_massachusetts_Data.pdf")

#There are other packages to help with pdf data scraping, but this one is easy for text. However, sorry about
#warnings, Pdfminer3k sets directly to the Python root logger :(

'''
Here is the stuff I need to mine

"State"
"SAT_Participation"
"SAT_English"
"SAT_Math"
"SAT_Total"

'''

import slate3k as slate

def pdf_mine(file):
    mine  = []
    with open(file, 'rb') as f:
        doc = slate.PDF(f)

    pdf_miner =  [x for x in doc[2].split("\n") if x != ""]
    #Sice these 51 pdf are exactly the same, but for the state SAT data, we can set the location
    #and mine from the lists
    for i in range(len(pdf_miner)):
        if i == 1:
            mine.append(pdf_miner[i].lstrip())
        elif pdf_miner[i][-14:] == '% of graduates':
            mine.append(pdf_miner[i].lstrip())

    pdf_miner = [x for x in doc[3].split("\n") if x != ""]
    for i in range(len(pdf_miner)):
        if pdf_miner[i].lstrip() == "Took Essay¹": #That little 1 helps!
            mine.append(pdf_miner[i + 12].lstrip())
            mine.append(pdf_miner[i + 10].lstrip())
            mine.append(pdf_miner[i + 14].lstrip())

    print(mine)
    return(mine)

print(pdf_mine('2018_SAT_massachusetts_Data.pdf'))


#The idea of this workflow is to set an empty dictionary and append all of the different SAT information
#To that file.

SAT_2018 = {}
for file in os.listdir():
    if file[0] != "A" and file[-3:] == "pdf":
        try:
            mine = pdf_mine(file)
            if file[-3:] == "pdf":
                SAT_2018[mine[0]] = {
                    "State":mine[0],

                    #I left the '% of graduates' below for inspection, need
                    #to strip now

                    "SAT_2018_Participation":float(mine[1].split("%")[0])/100,
                    "SAT_2018_English":int(mine[2]),
                    "SAT_2018_Math":int(mine[3]),
                    "SAT_2018_Total":int(mine[4])}
        except:
            print("something went wrong with {}".format(file))

sat2018 = pd.DataFrame.from_dict(SAT_2018, orient='index').reset_index()
sat2018.drop("index", axis = 1, inplace = True)
sat2018.head()

merged_2017_18 = pd.merge(merged, sat2018, on='State')
merged_2017_18.drop("Unnamed: 0", axis = 1, inplace = True)


#Done!
merged_2017_18.head()
