import json
from collections import Counter

with open('Series\\Summary.json', 'r') as file:#Will be set to series summary or go through each episode
    data = json.load(file)

def mergeDicts(*dicts):#Looking at profanity count dictionaries for a given character entry
    merged_dict = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if key in merged_dict:
                merged_dict[key] += value
            else:
                merged_dict[key] = value
    
    return merged_dict#dict a = {'f':5, 'g':2} dict b = {'f':2, 'h':1} return {'f':7, 'h':1, 'g':1}

def combineEntries(*dicts):
    lines, words, profanities, profCount = 0, 0, 0, {}
    for d in dicts: 
        if d in data:#If this name is in the dataset
            lines += data[d][0]#Increment each of these values
            words += data[d][1]
            profanities += data[d][2]
            profCount = mergeDicts(profCount, data[d][3])#Merge the profanity count dictionaries into one
            data.pop(d)#Remove their entry from the dataset
    combinedDict = [lines, words, profanities, dict(Counter(profCount).most_common()), (round(profanities/words * 100, 2))]#Put all the data together
    return combinedDict

combinedData = combineEntries('priest maxi', 'fr maxi', 'father maxi', 'maxi')
# print(combinedData)
data['priest maxi'] = combinedData#Assign the single entry in the dataset to the returned combined data
data = dict(sorted(data.items(), key=lambda x: x[1][0], reverse=True))#Sort dictionary so character with most lines is first

with open('Z.json', 'w') as f:
    f.write(json.dumps(data))

# cartman # kyle cartman # eric cartman
# kyle # kyle broflovski # kyle cartman # kyle ms crabtree
# stan # stan marsh # stan 
# chef # jerome chef mcelroy
# wendy # wendy testaburger
# liane # liane cartman
# ike # ike broflovski
# officer barbrady
# ms crabtree # ms veronica crabtree # kyle ms crabtree
# mr garrison # mr herbert garrison
# farmer carl # farmer carl denkins
# visitor # visitor carl
# mr kitty
# kenny # kenny mccormick
# mr hat
# boys
# train conductor
# news reporter
# cows
# blonde
# cow
# the boys
# kid
# jason


# if(temp[1] == 0):#Trying to get how often their words have profanities. If words == 0
#     temp[4] = 0#just add 0 to avoid divide by zero error
# else:
#     temp[4] = (round(temp[2]/temp[1] * 100, 2))#Append how often character uses profanity as a %. Profanities/Words 
