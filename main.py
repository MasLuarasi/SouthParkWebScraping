from bs4 import BeautifulSoup
from urllib.request import urlopen
from better_profanity import profanity
from collections import Counter
import re
import json
import time
import operator
import csv
import os

st = time.time()#Start time

def analyzeLine(line):#Count the number of words and profanities in the one line
    ret = [1]#1 as the first element representing the line. We also want to see how many lines each character has
    l = line.split(" ")#Split into list of words
    while("" in l):l.remove("")#Remove an empty elements in list that went through
    ret.append(len(l))#Length of list represents number of words in line
    profanityFrequency = []#Contains all the profanities for this line
    for word in l:#Library only checks if parameter has profanity, loop through split list from earlier to get total number
        if(profanity.contains_profanity(word) or (word[len(word)-1] == 's' and profanity.contains_profanity(word[:len(word)-1]))):#Some words in dictionary don't account for plural cases.
            profanityFrequency.append(word)#Add to list
    ret.append(len(profanityFrequency))#Add number of profanities in this line
    ret.append(profanityFrequency)#Add list of them
    return ret

def computeSeasonSummary(index, episodeTitles):#Add all the data from each episode in the season
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

    seasonSummary = dict(sorted(seasonSummary.items(), key=lambda x: x[1][0], reverse=True))#Sort dictionary so character with most lines is first

    with open('Seasons\\'+ str(index) +'\\Summary.json', 'w') as f:
        f.write(json.dumps(seasonSummary))#Create the season summary json file in the season folder with the contents in the dictionary
    with open('Series\\'+ str(index) +'Summary.json', 'w') as f:
        f.write(json.dumps(seasonSummary))#Create the season summary json file in the series folder with the contents in the dictionary
    f.close()
    writeToCSV(seasonSummary, ('Seasons\\' + str(index)), 'Summary')#Write the csv file for the season summary

def computeSeriesSummary():#Add all the data from each season summary into a series summary
    directory = 'Series/'#Navigate to folder
    if os.path.exists("Series\Summary.csv"):
        os.remove("Series\Summary.csv")
    if os.path.exists("Series\Summary.json"):
        os.remove("Series\Summary.json")
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
    writeToCSV(seriesSummary, 'Series\\' ,'Summary')

def writeToCSV(data, directory, titleFile):#Write the input data to a csv file
    csv_data = []
    for entry_name, entry_values in data.items():#Organizing to csv
        name = entry_name
        lines, words, profanityCount, profanityList, profanityFrequency = entry_values
        csv_data.append([name, lines, words, profanityCount, profanityList, profanityFrequency])#Data headers

    with open(directory +'\\' + titleFile + '.csv', 'w', newline="") as f:#Writing to csv
        writer = csv.writer(f)
        writer.writerow(["Name", "Lines", "Words", "Profanity Count", "Profanity List", "Profanity Frequency"])
        writer.writerows(csv_data) 
    f.close()

def main():
    heatmap = [[f"" for j in range(1, 21)] for i in range(1, 27)]
    with open("heatmap.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(heatmap)

    for index in range(1,27):#Seasons 1-26
        file = open("Seasons\\"+ str(index) + "\\Links.txt", "r")#URLs for episodes of each season are in Links.txt file in each seasons folder
        episodeLinks = file.read().split("\n")#Assign the URLs to episodeLinks
        file.close()

        episodeNumber = 1#Keep track so output json files are in correct order
        episodeTitles = []#Store episode titles here so we can assign file names correctly

        for episode in episodeLinks:
            characterData = dict()
            dialogue = []

            with urlopen(episode) as url:
                soup = BeautifulSoup(url, "lxml")#Get HTML of current episode

            element = soup.find("td", class_="headersthemes").get_text()#Trying to find the title of the episode
            title = element[1:element.find("/")]#Extract title name
            title = re.sub(r'[^\w\s]', '', title)#Discard any characters that are not allowed in file names.
            titleFile = ("".join([str(episodeNumber), "-", title]))#Modify it to be the format of the output text file
            episodeTitles.append(titleFile)

            print(titleFile)#Keep track of episode while running. If external error, we know which episodes html caused it
            episodeNumber += 1#Keep count so the files names maintain episode order

            lines = soup.find_all("tr")#Everything in the script is contained in <tr> elements
            for l in lines:#For each line(<tr> element)
                left = l.find("span", style="text-align:center; font-weight:bold; font-size:125%")#Getting html that displays character name(left side)
                if(left != None):#If it is not a scene description (Kind of, the html is not perfect, so some scene descriptions get through. We take care of that in next line)
                    if(left.find("center").get_text() != ''):#If the left side has an actual name(accounting for any mislabeled scene descriptions)
                        dialogue.append(l.get_text())#Get character name and their text

            for d in dialogue:
                s = d
                while('[' in s):#Scene descriptions are in []. Since they are not dialogue, remove them so they don't count.
                    start = s.find('[')
                    end = s.find(']') + 1
                    if(end == 0):#For instances where an opening '[' does not have a closing one/can't find closing one
                        s = s[:start]#Substring til the end cause all instances we've come across have it ending the text
                    else:
                        s = ("".join([s[:start], s[end:]]))#Substring from start to opening of scene description, with end of scene description to end of string   s[:start] + s[end:]
                lowered = s.lower().replace("-", " ")#Replace hyphens with space so words or stutters(Fucking Jimmy) don't get lost
                removedPunctuation = re.sub(r'[^\w\s]', '', lowered)#Remove punctuation from stirng

                characterAndDialogue = removedPunctuation.split("\n")#Format result to just be character name and dialogue, no \n. Split at new line so character name is first and what they say is second.
                characterAndDialogue[:] = [x for x in characterAndDialogue if x]#Remove empty elements in list
                if(len(characterAndDialogue) == 1): characterAndDialogue.append('i')#Very rare cases where the only "dialogue" in the script is an action in the '[]', so there would be no actual words to analyze, resulting in empty list
                # print(characterAndDialogue)#Debugging purposes
                # print("------------------------------------")#Debugging purposes. Visually separate contents of character and dialogue.
                lineWordProf = analyzeLine(characterAndDialogue[1])#Get the data for each line

                if(characterAndDialogue[0] in characterData):#If character already has an entry in the dictionary
                    for i in range(0,4):
                        characterData[characterAndDialogue[0]][i] += lineWordProf[i]#Increment the existing elements by the data found in the current line
                else:
                    characterData[characterAndDialogue[0]] = lineWordProf#Create a new entry and set it to the data found in the current line

            sortedCharacterDataByLines = dict(sorted(characterData.items(), key=lambda x: x[1], reverse=True))#Sorts characters by the number of lines

            names = sortedCharacterDataByLines.keys()#Temp variable containing the keys (character names)
            for k in names:#For each character
                values = sortedCharacterDataByLines.get(k)#Get their values(line, word, prof)
                if(values[1] == 0):#Trying to get how often their words have profanities. If words == 0
                    values.append(0)#just add 0 to avoid divide by zero error
                else:
                    values.append(round(values[2]/values[1] * 100, 2))#Append how often character uses profanity as a %. Profanities/Words 
                values[3] = dict(Counter(values[3]).most_common())#Count the frequency of each profanity. Replace the list in the character data with a dictionary that has profanity as key and number of times as value
                
            with open('Seasons\\'+ str(index) +'\\' + titleFile + '.json', 'w') as f:
                f.write(json.dumps(sortedCharacterDataByLines))#Write the final dictionary of the episode to a json file
            f.close()
            
            writeToCSV(sortedCharacterDataByLines, ('Seasons\\'+ str(index)), titleFile)#Write the data to a csv file as well
            
            # with open("heatmap.csv", "r", newline="") as file:
            #     reader = csv.reader(file)
            #     rows = list(reader)  # Read all rows from the CSV file

            # rows[index-1][int(titleFile.split('-')[0])-1] = next(iter(sortedCharacterDataByLines))  # Update the specified cell

            # with open("heatmap.csv", "w", newline="") as file:
            #     writer = csv.writer(file)
            #     writer.writerows(rows)  # Write all rows back to the CSV file

            time.sleep(2)#2 second sleeper to avoid overloading site with requests and getting booted

        computeSeasonSummary(index, episodeTitles)#Summarize the data across all episodes in a season

main()
# computeSeriesSummary()
et = time.time()#End time
print((et-st)*1000)#Total time for program to run
