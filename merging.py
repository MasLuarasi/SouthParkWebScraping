import os
import glob
import json
from collections import Counter
from natsort import natsorted

characterAlias = [
                ['butters', 'professor chaos', 'butters voice', 'butters '],
                ['carol', 'carol mccormick'],
                ['cartman', 'eric cartman', 'cartman as jennifer lopez', 'cartman smurf',
                 'cartman voiceover', 'cheesy poof cartman', ' cartman', 'coon', 'the coon',
                 'the boys', 'boys'],
                ['chef', 'jerome chef mcelroy', 'darth chef', 'chef falsetto'],
                ['clyde', 'clyde donovan', 'mosquito'],
                ['craig', 'craig tucker',],
                ['doctor', 'dr doctor'],
                ['gerald', 'geralds review', 'gerald broflovski'],
                ['ike', 'ike broflovski',],
                ['jesus', 'jesus christ',],
                ['jimbo', 'uncle jimbo'],
                ['jimmy', 'jimmy valmer'],
                ['kenny', 'kenny mccormick', 'mysterion', 'the boys', 'boys'],
                ['kyle', 'kyle broflovski', 'kyle voiceover', 'human kite', 
                 'the human kite', 'the boys', 'boys'],
                ['liane', 'liane cartman'],
                ['mayor mcdaniels', 'mayor mcdaneils', 'mayor mcdanniels', 'mayor'],
                ['mr garrison', 'mrs garrison', 'garrison', 'herbert garrison',
                 'clean garrison', 'unkempt garrison', 'ms garrison', 'mr herbert garrison',
                 'president garrison', 'mrgarrison', 'mr garrison '],
                ['mr mackey', 'mackey', 'mrmackey'],
                ['officer barbrady', 'barbrady'],
                ['priest maxi', 'fr maxi', 'father maxi', 'maxi'],
                ['principal victoria', 'pricipal victoria'],
                ['randy', 'randy marsh', 'randy singing', 'lorde'],
                ['santa', 'santa claus'],
                ['scott', 'scott malkinson'],
                ['sharon', 'sharon marsh', 'sharon '],
                ['sheila', 'sheila broflovski'],
                ['shelly', 'shelly marsh'],
                ['stan', 'stan marsh', 'stan ', 'toolshed', 'the boys', 'boys'],
                ['stephen', 'stephen stotch'],
                ['stuart', 'stuart mccormick'],
                ['timmy', 'timmy burch', 'iron maiden'],
                ['tolkien', 'tolkien black', 'tuperwear'],
                ['tweek', 'tweek tweak'],
                ['wendy', 'wnedy testaburger', 'human wendy'],
                ['yates', 'sgt yates', 'det yates', 'sergeant yates', 'yatess']
                ]           

# with open('Series\\Summary.json', 'r') as file:#Will be set to series summary or go through each episode
#     data = json.load(file)

def mergeDicts(*dicts):#Looking at profanity count dictionaries for a given character entry
    merged_dict = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if key in merged_dict:
                merged_dict[key] += value
            else:
                merged_dict[key] = value
    
    return merged_dict#dict a = {'f':5, 'g':2} dict b = {'f':2, 'h':1} return {'f':7, 'h':1, 'g':1}

def combineEntries(characterList):
    lines, words, profanities, profCount, profFreq = 0, 0, 0, {}, 0
    for d in characterList:
        if d in data:#If this name is in the dataset
            lines += data[d][0]#Increment each of these values
            words += data[d][1]
            profanities += data[d][2]
            profCount = mergeDicts(profCount, data[d][3])#Merge the profanity count dictionaries into one
            if(words == 0):#Trying to get how often their words have profanities. If words == 0
                profFreq = 0#just add 0 to avoid divide by zero error
            else:
                profFreq = (round(profanities/words * 100, 2))#Append how often character uses profanity as a %. Profanities/Words 
            data.pop(d)
    return [lines, words, profanities, dict(Counter(profCount).most_common()), profFreq]#Return all the data together

for index in range(1, 27):
    filePath = os.path.join('Seasons\\', str(index))#'Seasons\1...
    if os.path.exists(filePath):
        epFiles = natsorted(glob.glob(os.path.join(filePath, '*.json')))#Gather all the json files
        for ep in epFiles:#For each episode in this season
            with open(ep, 'r') as file:
                data = json.load(file)
                for c in characterAlias:#For every character list in the characterAlias list
                    data[c[0]] = combineEntries(c)#Assign the single entry in the dataset to the returned combined data
                data = dict(sorted(data.items(), key=lambda x: x[1][0], reverse=True))#Sort dictionary after all changes so character with most lines is first
                with open(ep, 'w') as f:
                    f.write(json.dumps(data))

#NEXT STEPS
#List for characters could be a text file
