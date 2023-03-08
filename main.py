from bs4 import BeautifulSoup
from urllib.request import urlopen
from better_profanity import profanity
from collections import OrderedDict
from collections import Counter
import re
import json
import time
import operator

file = open("Seasons\\Movie\\Links.txt", "r")
episodeLinks = file.read().split("\n")
file.close()

episodeNumber = 1

def analyzeLine(line):#Count the number of words and profanities in the one line
    ret = [1]#1 as the first element representing the line. We also want to see how many lines each character has
    l = line.split(" ")#Split into list of words and add length of the split to list
    while("" in l):l.remove("")#Remove an empty elements in list that went through
    ret.append(len(l))#Length of list represents number of words in line
    profanityFrequency = []#Contains all the profanities for this line
    for word in l:#Library only checks if parameter has profanity, loop through split list from earlier to get total number
        if(profanity.contains_profanity(word) or (word[len(word)-1] == 's' and profanity.contains_profanity(word[:len(word)-1]))):#Some words in dictionary don't account for plural cases.
            profanityFrequency.append(word)#Add to list
    ret.append(len(profanityFrequency))#Add number of profanities in this line
    ret.append(profanityFrequency)#Add list of them
    return ret

for episode in episodeLinks:
    time.sleep(2)
    characterData = dict()
    dialogue = []

    with urlopen(episode) as url:
        soup = BeautifulSoup(url, "lxml")

    element = soup.find("td", class_="headersthemes").get_text()#Trying to get the title of the episode
    title = element[1:element.find("/")]#Extract title name
    titleFile = ("".join([str(episodeNumber), "-", title]))#Modify it to be the format of the output text file
    if(':' in titleFile): titleFile = titleFile.replace(':', '')#In case the title has a ':' in it, remove it since file names can't have colons in names
    print(titleFile)

    episodeNumber += 1

    lines = soup.find_all("tr")#Everything in the script is contained in <tr> elements
    for l in lines:
        if(l.find("span", style="font-size:110%") != None):#Only care about the cases where there is actual dialogue.
            dialogue.append(l.get_text())#Get character name and their text

    for d in dialogue:
        s = d
        while('[' in s):#Scene descriptions are in []. Since they are not dialogue, remove them so they don't count.
            start = s.find('[')
            end = s.find(']') + 1
            if(end == 0):#Couple instances where an opening '[' does not have a closing one. If it can't find closing one
                s = s[:start]#Substring til the end cause all instances we've come across have it ending the text
            else:
                s = ("".join([s[:start], s[end:]]))#Substring from start to opening of scene description, with end of scene description to end of string   s[:start] + s[end:]
        lowered = s.lower().replace("-", " ")#Replace hyphens with space so words or stutters(F Jimmy) don't get lost
        removedPunctuation = re.sub(r'[^\w\s]', '', lowered)#Remove punctuation from stirng

        characterAndDialogue = removedPunctuation.split("\n")#Format result to just be character name and dialogue, no \n. Split at new line so character name is first and what they say is second.
        while("" in characterAndDialogue): 
            characterAndDialogue.remove("")#Remove empty elements in list

        if(len(characterAndDialogue) == 1): characterAndDialogue.append('i')#Very rare cases where the only "dialogue" on the script is an action in the '[]', so there would be no actual words to analyze

        lineWordProf = analyzeLine(characterAndDialogue[1])#Get the data for each line

        if(characterAndDialogue[0] in characterData):#If character already has an entry in the dictionary
            for i in range(0,3):
                characterData[characterAndDialogue[0]][i] += lineWordProf[i]#Increment the existing elements by the data found in the current line
            if(lineWordProf[3] != None):#If the profanity frequency dictionary is not empty
                characterData[characterAndDialogue[0]][3] += lineWordProf[3]#Add the profanities from the line we just analyzed
        else:
            characterData[characterAndDialogue[0]] = lineWordProf#Create a new entry and set it to the data found in the current line

    sortedCharacterDataByLines = sorted(characterData.items(), key=operator.itemgetter(1), reverse=True)#Sort dictionary so character with most lines is first

    for i in range(len(sortedCharacterDataByLines)):
        t = sortedCharacterDataByLines[i][1]#Temp variable
        t.append(round(t[2]/t[1] * 100, 2))#Append the frequency of profanities as a %. Profanities/Words
        t[3] = OrderedDict(Counter(t[3]).most_common())#Count the frequency of each profanity. Replace the list in the character data with a dictionary that has profanity as key and frequency as value

    with open('Seasons\\Movie\\' + titleFile + '.json', 'w') as convert_file:
        convert_file.write(json.dumps(sortedCharacterDataByLines))


# Bugs to fix
#Write all p's to array, then at the part where we were working with Aadya count them and sort them.

    # profanityFrequency = dict()
    # for word in l:#Library only checks if parameter has profanity, loop through split list from earlier to get total number
    #     if(profanity.contains_profanity(word) or (word[len(word)-1] == 's' and profanity.contains_profanity(word[:len(word)-1]))):#Some words in dictionary don't account for plural cases.
    #         profanityCount += 1
    #         if word in profanityFrequency:#If profanity has more than one occurence in the line
    #             profanityFrequency[word] += 1#Increment the value for it by one
    #         else:
    #             profanityFrequency[word] = 1#Create a new entry and set it to one


                # for p in lineWordProf[3]:#For every word in the profanity frequency dictionary
                #     characterData[characterAndDialogue[0]][3].append(p)
                    # if (p in characterData[characterAndDialogue[0]][3]):#If that profanity already exists in that characters profanity frequency dictionary
                    #     characterData[characterAndDialogue[0]][3][p] += 1#Increment the value for the key in the dictionary by one
                    # else:
                    #     characterData[characterAndDialogue[0]][3][p] = 1#Create a new entry and set it to one

    # for i in range(len(sortedCharacterDataByLines)):
    #     sortedCharacterDataByLines[i][1][3] = dict(sorted(sortedCharacterDataByLines[i][1][3].items(), key=operator.itemgetter(1), reverse=True))#For each character, sort their profanity frequency dictionary so most common used ones are first 
