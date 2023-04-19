import os
import json
from collections import Counter
import json
import operator


def computeSeriesSummary():#Add all the data from each season summary into a series summary
    directory = 'Series/'#Navigate to folder
    seriesSummary = dict()
    for filename in os.listdir(directory):#For each seasonSummary in the directory
        current = dict(json.load(open(os.path.join(directory, filename))))#Get the data of current seasonSummary
        for c in current:#For each key
            if(c in seriesSummary.keys()):#If character already has an entry in the dictionary, so if they were in one of previous episodes
                for j in range(0,3):
                    seriesSummary[c][j] += current[c][j]#Update lines, words, and profanity count
                seriesSummary[c][4] = round(seriesSummary[c][2]/seriesSummary[c][1] * 100, 2)#Update the profanity % with updated words and profanity count data
                seriesSummary[c][3] = dict(sorted((Counter(seriesSummary[c][3]) + Counter(current[c][3])).items(), key=operator.itemgetter(1), reverse=True))#Merge the profanity frequency dictionaries and sort in descending order 
            else:
                seriesSummary[c] = current[c]#Make a new entry

    seriesSummary = dict(sorted(seriesSummary.items(), key=lambda x: x[1][0], reverse=True))#Sort dictionary so character with most lines is first

    with open('Series/Summary.json', 'w') as f:
        f.write(json.dumps(seriesSummary))#Create the series summary json file with the contents in the dictionary
    f.close()

computeSeriesSummary()
