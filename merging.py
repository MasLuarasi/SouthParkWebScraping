import json
from collections import Counter
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def merge_dicts(*dicts):
    merged_dict = {}
    
    for dictionary in dicts:
        for key, value in dictionary.items():
            if key in merged_dict:
                merged_dict[key] += value
            else:
                merged_dict[key] = value
    
    return merged_dict

with open('Series\\Summary.json', 'r') as file:
    data = json.load(file)
#'Seasons\\1\\1-Cartman Gets an Anal Probe.json'
# data['Eric Cartman'] = [0, 0, 0, {}, 0.0]

# temp = data['Eric Cartman']

# for i in range(0,3):
#     temp[i] = data['cartman'][i] + data['eric cartman'][i]

# if(temp[1] == 0):#Trying to get how often their words have profanities. If words == 0
#     temp[4] = 0#just add 0 to avoid divide by zero error
# else:
#     temp[4] = (round(temp[2]/temp[1] * 100, 2))#Append how often character uses profanity as a %. Profanities/Words 

# merged_dict = merge_dicts(data['cartman'][3], data['eric cartman'][3])
# temp[3] = merged_dict

# temp[3] = dict(Counter(temp[3]).most_common())#Count the frequency of each profanity. Replace the list in the character data with a dictionary that has profanity as key and number of times as value

# print(data["Eric Cartman"])

for key1 in data:
    for key2 in data:
        if data[key1][0] > 50 and key1 != key2 and data[key1][0] >= data[key2][0] and data[key1][1] >= data[key2][1]:
            combined_key = key1 + '\t' + key2
            simPercent = similar(key1, key2)
            if(simPercent > .5 and key1 in key2):
                print(combined_key + '\t' + str(similar(key1, key2)))



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
