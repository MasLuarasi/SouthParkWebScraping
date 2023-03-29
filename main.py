from bs4 import BeautifulSoup
from urllib.request import urlopen
from better_profanity import profanity
from collections import Counter
import re
import json
import time
import operator

st = time.time()

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

def computeSummary(index):#Add all the data from each episode in the season
    seasonSummary = dict()
    for e in episodeTitles:#Subsequent episodes and their data
        current =  json.load(open('Seasons\\'+ str(index) +'\\' + e + '.json'))#Get the data of current episode
        for c in current:#For each key
            if(c in seasonSummary.keys()):#If character already has an entry in the dictionary, so if they were in one of previous episodes
                for j in range(0,3):
                    seasonSummary[c][j] += current[c][j]#Update lines, words, and profanity count
                seasonSummary[c][4] = round(seasonSummary[c][2]/seasonSummary[c][1] * 100, 2)#Update the profanity % with updated words and profanity count data
                seasonSummary[c][3] = dict(sorted((Counter(seasonSummary[c][3]) + Counter(current[c][3])).items(), key=operator.itemgetter(1), reverse=True))#Merge the profanity frequency dictionaries and sort in descending order 
            else:
                seasonSummary[c] = current[c]#Make a new entry

    seasonSummary = dict(sorted(seasonSummary.items(), key=lambda x: x[1][0], reverse=True))
    # seasonSummary = dict(sorted(seasonSummary.items(), key=operator.itemgetter(1), reverse=True))#Sort dictionary so character with most lines is first

    with open('Seasons\\'+ str(index) +'\\Summary.json', 'w') as f:
        f.write(json.dumps(seasonSummary))
    f.close()


for index in range(20,27):
    print(index)
    file = open("Seasons\\"+ str(index) + "\\Links.txt", "r")
    episodeLinks = file.read().split("\n")
    file.close()

    episodeNumber = 1
    episodeTitles = []

    for episode in episodeLinks:
        characterData = dict()
        dialogue = []

        with urlopen(episode) as url:
            soup = BeautifulSoup(url, "lxml")

        element = soup.find("td", class_="headersthemes").get_text()#Trying to get the title of the episode
        title = element[1:element.find("/")]#Extract title name
        title = re.sub(r'[^\w\s]', '', title)
        titleFile = ("".join([str(episodeNumber), "-", title]))#Modify it to be the format of the output text file
        # if(':' or '?' in titleFile): titleFile = titleFile.replace(':' or '?', '')#In case the title has a ':' in it, remove it since file names can't have colons in names
        episodeTitles.append(titleFile)

        print(titleFile)
        episodeNumber += 1#Keep count so the files names maintain episode order

        lines = soup.find_all("tr")#Everything in the script is contained in <tr> elements
        for l in lines:
            left = l.find("span", style="text-align:center; font-weight:bold; font-size:125%")#Getting html that displays character name(left side)
            if(left != None):#If it is not a scene description (Kind of, the html is not perfect, so some scene descriptions get through. We take care of that in a sec)
                if(left.find("center").get_text() != ''):#If the left side has an actual name(accounting for any mislabeled scene descriptions)
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
            lowered = s.lower().replace("-", " ")#Replace hyphens with space so words or stutters(Fucking Jimmy) don't get lost
            removedPunctuation = re.sub(r'[^\w\s]', '', lowered)#Remove punctuation from stirng

            characterAndDialogue = removedPunctuation.split("\n")#Format result to just be character name and dialogue, no \n. Split at new line so character name is first and what they say is second.
            characterAndDialogue[:] = [x for x in characterAndDialogue if x]#Remove empty elements in list
            if(len(characterAndDialogue) == 1): characterAndDialogue.append('i')#Very rare cases where the only "dialogue" on the script is an action in the '[]', so there would be no actual words to analyze
            # print(characterAndDialogue)
            # print("------------------------------------")
            lineWordProf = analyzeLine(characterAndDialogue[1])#Get the data for each line

            if(characterAndDialogue[0] in characterData):#If character already has an entry in the dictionary
                for i in range(0,4):
                    characterData[characterAndDialogue[0]][i] += lineWordProf[i]#Increment the existing elements by the data found in the current line
            else:
                characterData[characterAndDialogue[0]] = lineWordProf#Create a new entry and set it to the data found in the current line

        sortedCharacterDataByLines = dict(sorted(characterData.items(), key=lambda x: x[1], reverse=True))

        names = sortedCharacterDataByLines.keys()#Temp variable containing the keys (character names)
        for k in names:
            values = sortedCharacterDataByLines.get(k)
            if(values[1] == 0): 
                values.append(0)
            else:
                values.append(round(values[2]/values[1] * 100, 2))#Append the frequency of profanities as a %. Profanities/Words 
            values[3] = dict(Counter(values[3]).most_common())#Count the frequency of each profanity. Replace the list in the character data with a dictionary that has profanity as key and frequency as value
            
        with open('Seasons\\'+ str(index) +'\\' + titleFile + '.json', 'w') as f:
            f.write(json.dumps(sortedCharacterDataByLines))#Write the episode data to json file
        
        time.sleep(2)


    f.close()
    computeSummary(index)

et = time.time()
print((et-st)*1000)


# Bugs to fix
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


            # if(lineWordProf[3] != None):#If the profanity frequency dictionary is not empty
            #     characterData[characterAndDialogue[0]][3] += lineWordProf[3]#Add the profanities from the line we just analyzed

#Worked: 11, 
#Not All: 3/4, 12/13/14, 17, 
#No Sum: The rest

