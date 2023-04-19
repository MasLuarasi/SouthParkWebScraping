import json
from collections import Counter
import json

def printFirstTen(d, index):#Print first ten elements of input dictionary and the specified dictionary value
    topTen = {}
    for i, key in enumerate(d.keys()):#Iterate through dictionary via keys
        if i < 10:
            topTen[key] = d[key][index]#Assign key and specific data value in topTen dictionary
        else:
            break
    print(topTen)


seriesSummary = json.load(open("Series\Summary.json"))#Series summary sorted by number of lines per character
printFirstTen(seriesSummary, 0)#Get top 10 characters by line

seriesByWords = dict(sorted(seriesSummary.items(), key=lambda x: x[1][1], reverse=True))#Sort dictionary so character with most words is first
printFirstTen(seriesByWords, 1)#Get top 10 characters by words

seriesByProfanityCount = dict(sorted(seriesSummary.items(), key=lambda x: x[1][2], reverse=True))#Sort dictionary so character with most profanity count is first
printFirstTen(seriesByProfanityCount, 2)#Get top 10 characters by profanity count

seriesByProfanityFreq = dict(sorted(seriesSummary.items(), key=lambda x: x[1][4], reverse=True))#Sort dictionary so character with highest profanity frequency is first
delete = [key for key in seriesByProfanityFreq if seriesByProfanityFreq[key][0] < 100]#Create record of any characters that have less than 100 lines
for key in delete:
    del seriesByProfanityFreq[key]#Delete those ones since it is not enough data
printFirstTen(seriesByProfanityFreq, 4)#Get top 10 characters by profanity frequency
